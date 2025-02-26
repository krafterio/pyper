# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class ResConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    block_assignation_mail = fields.Boolean(
        'Block assignation mail',
        config_parameter='pyper.block_assignation_mail',
    )

    block_all_assignation_mail = fields.Boolean(
        'Block all assignation mail',
        config_parameter='pyper.block_all_assignation_mail',
    )

    models_to_block = fields.Many2many(
        'ir.model',
        string="Models to Block",
        help="Select models for which assignation emails should be blocked",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        models_to_block_ids = self.env['ir.config_parameter'].sudo().get_param('pyper.models_to_block')
        if models_to_block_ids:
            res['models_to_block'] = [(6, 0, [int(model_id) for model_id in models_to_block_ids.split(',')])]
        return res

    def set_values(self):
        super().set_values()
        models_to_block_ids = [str(model.id) for model in self.models_to_block]
        self.env['ir.config_parameter'].sudo().set_param('pyper.models_to_block', ','.join(models_to_block_ids))
