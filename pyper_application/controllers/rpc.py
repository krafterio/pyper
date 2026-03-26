# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo.http import Controller, route, dispatch_rpc


class Rpc(Controller):
    @route('/app-ext/jsonrpc', type='jsonrpc', auth='none', cors='*', save_session=False)
    def jsonrpc(self, service, method, args):
        return dispatch_rpc(service, method, args)
