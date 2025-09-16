# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(IrHttp, self).session_info()

        if self.env.user.has_group('base.group_user'):
            ICP = self.env['ir.config_parameter'].sudo()
            provider = ICP.get_param('pyper_map.provider', False)
            res.update(
                pyper_map_provider=provider,
                pyper_map_provider_token=ICP.get_param('pyper_map.' + provider + '.token', False),
            )

        return res
