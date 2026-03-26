# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.addons.mail.controllers.thread import ThreadController as BaseThreadController


class ThreadController(BaseThreadController):
    @http.route('/mail/thread/messages', methods=['POST'], type='jsonrpc', auth='user')
    def mail_thread_messages(self, thread_model, thread_id, fetch_params=None):
        if self._include_children_messages(thread_model):
            request.update_context(mail_message_with_children_res_ids=request.env[thread_model].search([('parent_id', '=', thread_id)]).ids)

        return super().mail_thread_messages(thread_model, thread_id, fetch_params)

    def _include_children_messages(self, thread_model):
        return thread_model == 'res.partner'
