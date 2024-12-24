# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import pytz

from odoo import api, fields, models, Command
from odoo.tools import email_split


class MailMessage(models.Model):
    _inherit = 'mail.message'

    restrict_access = fields.Boolean(
        string='Restrict Access',
    )

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """Called by ``message_process`` when a new message is received
           for a given thread model, if the message did not belong to
           an existing thread.
           The default behavior is to create a new record of the corresponding
           model (based on some very basic info extracted from the message).
           Additional behavior may be implemented by overriding this method.

           :param dict msg_dict: a map containing the email details and
                                 attachments. See ``message_process`` and
                                ``mail.message.parse`` for details.
           :param dict custom_values: optional dictionary of additional
                                      field values to pass to create()
                                      when creating the new thread record.
                                      Be careful, these values may override
                                      any other values coming from the message.
           :rtype: int
           :return: the id of the newly created message object
        """
        data = {}

        if isinstance(custom_values, dict):
            data = custom_values.copy()

        # Find mail server from context
        mail_server_id = self.env.context.get('fetchmail_server_id', False)
        mail_server = self.env['fetchmail.server']

        if mail_server_id:
            mail_server = mail_server.browse(mail_server_id)

        # Skip if mail server is not found or sync all is disabled
        if not mail_server or not mail_server.sync_all:
            return self.env['mail.message']

        # Skip message creation if message already exist
        message_id = msg_dict.get('message_id', False)
        existing_msg = self.env['mail.message'].sudo().search([
            ('mail_server_id', '=', mail_server.id),
            ('message_id', '=', message_id),
        ], limit=1)

        if existing_msg:
            return existing_msg

        # Find message author
        from_mail_addresses = email_split(msg_dict.get('from', ''))
        from_partners = self.env['mail.thread']._mail_find_partner_from_emails(from_mail_addresses, force_create=True)
        author = from_partners[0] if from_partners else self.env.user.partner_id

        # Find message main readers
        to_mail_addresses = email_split(msg_dict.get('to', ''))
        reader_partners = self.env['mail.thread']._mail_find_partner_from_emails(to_mail_addresses, force_create=True)
        reader = reader_partners[0] if reader_partners else False

        # Find message copy carbon readers
        cc_mail_addresses = email_split(msg_dict.get('cc', ''))
        cc_partners = self.env['mail.thread']._mail_find_partner_from_emails(cc_mail_addresses, force_create=True)

        # Find message recipients
        recipient_addresses = email_split(msg_dict.get('recipients', ''))
        recipient_partners = self.env['mail.thread']._mail_find_partner_from_emails(recipient_addresses, force_create=True)

        # Merge all found partners in author, main readers, copy carbon readers and recipients
        partner_ids_set = set()
        partners = []

        if author and author.id not in partner_ids_set:
            partners.append(Command.link(author.id))
            partner_ids_set.add(author.id)

        if reader and reader.id not in partner_ids_set:
            partners.append(Command.link(reader.id))
            partner_ids_set.add(reader.id)

        for cc_partner in cc_partners:
            if cc_partner.id not in partner_ids_set:
                partners.append(Command.link(cc_partner.id))
                partner_ids_set.add(cc_partner.id)

        for recipient_partner in recipient_partners:
            if recipient_partner.id not in partner_ids_set:
                partners.append(Command.link(recipient_partner.id))
                partner_ids_set.add(recipient_partner.id)

        # Add mail server user partner in partners (to allow access)
        if mail_server.user_id.partner_id.id not in partner_ids_set:
            partners.append(Command.link(mail_server.user_id.partner_id.id))
            partner_ids_set.add(mail_server.user_id.partner_id.id)

        # Find first recipient
        first_recipient_id = False

        for partner in partners:
            if partner[1] != author.id:
                first_recipient_id = partner[1]
                break

        if not first_recipient_id and len(partners) > 1:
            first_recipient_id = partners[0][1]

        # Find message type
        message_type = 'email_outgoing' if author and author.id == mail_server.user_id.partner_id.id else 'email'

        # Find parent message
        references = msg_dict.get('references', '').split()
        parent_id = self.env['mail.message']

        if references:
            parent_message = self.env['mail.message'].sudo().search([('message_id', 'in', references)], limit=1)
            if parent_message:
                parent_id = parent_message

        # Format date
        tmz = pytz.timezone(self.env.user.tz or 'UTC')
        date = fields.Datetime.from_string(msg_dict.get('date')) if msg_dict.get('date') else False
        date = date.astimezone(tmz).replace(tzinfo=None) if date else False

        # Prepare message data
        data.update({
            'is_internal': True,
            'mail_server_id': mail_server.id,
            'message_id': message_id,
            'date': date,
            'record_name': False,
            'message_type': message_type,
            'subtype_id': self.env.ref('mail.mt_activities').id,
            'mail_activity_type_id': self.env.ref('mail.mail_activity_data_email').id,
            'email_from': msg_dict.get('email_from', False),
            'author_id': author.id,
            'reply_to': False,
            'reply_to_force_new': False,
            'restrict_access': True,
            'partner_ids': partners,
            'subject': msg_dict.get('subject', False),
            'body': msg_dict.get('body', False),
            'parent_id': parent_id.id,
            'model': 'res.partner',
            'res_id': first_recipient_id,
        })

        res = self.env['mail.message'].sudo().create(data)

        # Create and link attachments
        attachments = []
        for email_attachment in msg_dict.get('attachments', []):
            attachment = self.env['ir.attachment'].create({
                'name': email_attachment.fname,
                'raw': email_attachment.content,
                'mimetype': email_attachment.info.get('encoding') if email_attachment.info else None,
                'type': 'binary',
                'res_model': 'mail.message',
                'res_id': res.id,
                'access_partner_ids': partners,
            })
            attachments.append(Command.link(attachment.id))

        if attachments:
            res.attachment_ids = attachments

        return res

    def _creation_subtype(self):
        """Creation subtype is called when new message is created.
        """
        return self.env['mail.message.subtype']

    def message_update(self, msg_dict, update_vals=None):
        """Update of message must never be run when email is imported, but it is called just after the creation.
        """
        if update_vals:
            self.write(update_vals)

        return True

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_xmlid=None, subtype_id=False, partner_ids=None,
                     attachments=None, attachment_ids=None, body_is_html=False,
                     **kwargs):
        """Skip message post when email is imported.
        """
        return None


    @api.model
    def _message_fetch(self, domain, search_term=None, before=None, after=None, around=None, limit=30):
        if len(domain) > 2 and domain[0][0] == 'res_id' and domain[0][1] == '=' and domain[1][0] == 'model' and domain[1][1] == '=' and domain[1][2] == 'res.partner':
            res_id_filter = domain[0]
            extended_res_domain = [
                '|',
                ('partner_ids', 'child_of', res_id_filter[2]),
                res_id_filter,
                '&',
            ]
            del domain[0]
            domain[:0] = extended_res_domain

        return super()._message_fetch(domain, search_term, before, after, around, limit)
