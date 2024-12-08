# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.addons.mail.controllers.thread import ThreadController as BaseThreadController


class ThreadController(BaseThreadController):
    @http.route('/mail/thread/messages', methods=['POST'], type='json', auth='user')
    def mail_thread_messages(self, thread_model, thread_id, search_term=None, before=None, after=None, around=None, limit=30, audit_log=False):
        if not audit_log:
            domain = [
                ('res_id', '=', int(thread_id)),
                ('model', '=', thread_model),
                ('message_type', '!=', 'user_notification'),
                ('is_audit_log', '=', False),
            ]
            res = request.env['mail.message']._message_fetch(domain, search_term=search_term, before=before, after=after, around=around, limit=limit)

            if not request.env.user._is_public():
                res['messages'].set_message_done()

            return {**res, 'messages': res['messages'].message_format()}

        return super(ThreadController, self).mail_thread_messages(thread_model, thread_id, search_term, before, after, around, limit)
