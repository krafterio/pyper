# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import email
import locale
import logging
import pytz

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    user_id = fields.Many2one(
        'res.users',
        string='User',
    )

    sync_all_available = fields.Boolean(
        'Sync All Available Emails',
        compute='_compute_sync_all_available',
        store=True,
    )

    sync_all = fields.Boolean(
        string='Sync All Emails',
    )

    sync_all_message_ids = fields.Json(
        'Sync All Message Ids',
        help='The remaining message IDs to retrieve from the server',
    )

    @api.depends('server_type')
    def _compute_sync_all_available(self):
        for server in self:
            server.sync_all_available = server._get_connection_type() == 'imap'

    @api.onchange('server_type')
    def _onchange_server_type(self):
        for server in self:
            if not server.sync_all_available:
                server.sync_all = False
                server.user_id = False

    @api.onchange('sync_all')
    def _onchange_sync_all(self):
        for server in self:
            if server.sync_all:
                server.object_id = self.env['ir.model'].search([('model', '=', 'mail.message')], limit=1)
            else:
                server.object_id = False

            # Reset the last date of sync when sync all field is edited
            server.date = False

    @api.onchange('user', 'server_type')
    def _onchange_user(self):
        for server in self:
            if server.sync_all_available:
                # Search res.users with username of server
                server.user_id = self.env['res.users'].search([('login', '=', server.user)], limit=1)

                if not server.user_id:
                    server.user_id = self.env.user

                    if not server.user:
                        server.user = server.user_id.login

    def fetch_mail(self):
        """ WARNING: meant for cron usage only - will commit() after each email! """
        sync_all_servers = self.filtered(lambda fms: fms._get_connection_type() == 'imap' and fms.sync_all)
        other_servers = self.filtered(lambda fms: not (fms._get_connection_type() == 'imap' and fms.sync_all))

        # Fetch other servers and sync all servers
        res_other = super(FetchmailServer, other_servers).fetch_mail()
        res_sync_all_imap = self._fetch_all_imap_mail(sync_all_servers)

        return res_other and res_sync_all_imap

    def _fetch_all_imap_mail(self, servers):
        # Fetch IMAP email servers
        additionnal_context = {
            'fetchmail_cron_running': True,
        }
        MailThread = self.env['mail.thread']
        for server in servers:
            _logger.info('start checking for new emails on %s server %s', server.server_type, server.name)
            additionnal_context['default_fetchmail_server_id'] = server.id
            additionnal_context['fetchmail_server_id'] = server.id
            additionnal_context['fetchmail_server_type'] = server.server_type
            count, failed = 0, 0
            imap_server = None
            last_date = None

            try:
                imap_server = server.connect()
                folder = self._find_all_email_folder(imap_server) or 'INBOX'
                imap_server.select(folder)

                # Retrieve emails ids to be sync
                srv_last_date = server.date
                srv_email_ids = server.sync_all_message_ids
                if not srv_email_ids:
                    search_filter = server._get_search_email_filter()
                    result, data = imap_server.search(None, search_filter)
                    srv_email_ids = [int(email_id) for email_id in data[0].split()]

                for num in srv_email_ids.copy():
                    result, data = imap_server.fetch(str(num), '(RFC822)')

                    try:
                        # Retrieve the last date from email
                        msg = email.message_from_bytes(data[0][1])
                        last_date = email.utils.parsedate_to_datetime(msg['Date']) if 'Date' in msg else None

                        if last_date:
                            tmz = pytz.timezone(self.env.user.tz or 'UTC')
                            last_date = last_date.astimezone(tmz).replace(tzinfo=None)

                        # Process message only if message date is greater than or equal the server date
                        # because IMAP search accept only a date format
                        if not server.date or last_date >= server.date:
                            MailThread.with_context(**additionnal_context).message_process(
                                server.object_id.model,
                                data[0][1],
                                save_original=server.original,
                                strip_attachments=(not server.attach)
                            )
                    except Exception:
                        _logger.info('Failed to process mail from %s server %s.', server.server_type, server.name,
                                     exc_info=True)
                        failed += 1

                    # Update server info with messages still to be obtained
                    srv_email_ids.remove(num)
                    if len(srv_email_ids) == 0:
                        srv_email_ids = False

                    if not srv_last_date or last_date > srv_last_date:
                        srv_last_date = last_date

                    server.write({
                        'sync_all_message_ids': srv_email_ids,
                        'date': fields.Datetime.to_string(srv_last_date),
                    })

                    self._cr.commit()
                    count += 1
                _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count, server.server_type,
                             server.name, (count - failed), failed)
            except Exception:
                _logger.info("General failure when trying to fetch mail from %s server %s.", server.server_type,
                             server.name, exc_info=True)
            finally:
                if imap_server:
                    try:
                        imap_server.close()
                        imap_server.logout()
                    except OSError:
                        _logger.warning('Failed to properly finish imap connection: %s.', server.name, exc_info=True)

        return True

    @staticmethod
    def _find_all_email_folder(imap_server):
        status, folders = imap_server.list()
        if status == 'OK':
            for folder in folders:
                dec_folder = folder.decode()
                parts = dec_folder.split(' "/" ')
                attributes = parts[0].strip()
                folder_name = parts[1].strip('"')

                if '\\All' in attributes:
                    return f'"{folder_name}"'

        return None

    def _get_search_email_filter(self):
        self.ensure_one()

        # Retrieve all emails or all emails since the last sync date formatted in EN locale
        search_filter = 'ALL'
        if self.date:
            current_locale = locale.getlocale(locale.LC_TIME)
            try:
                locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
                search_filter = f'SINCE "{self.date.strftime('%d-%b-%Y').upper()}"'
            finally:
                locale.setlocale(locale.LC_TIME, current_locale)

        return search_filter
