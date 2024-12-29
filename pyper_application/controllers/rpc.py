# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.http import Controller, route, dispatch_rpc


class Rpc(Controller):
    @route('/app-ext/jsonrpc', type='json', auth='none', cors='*', save_session=False)
    def jsonrpc(self, service, method, args):
        return dispatch_rpc(service, method, args)
