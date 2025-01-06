# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, Command


class CollectionsRemoveWizard(models.TransientModel):
    _name = 'ir.collections.wizard'
    _description = 'Collection wizard'

    collection_id = fields.Many2one(
        'ir.collections',
        'Collection',
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_action_id = self.env.context.get('active_action_id', False)

        if not self.env.context.get('link_action', False) and active_action_id:
            defaults.update({
                'collection_id': self.env['ir.actions.act_window'].browse(active_action_id).ir_collections_id.id,
            })

        return defaults

    def save(self):
        model = self.env.context.get('active_model')
        ids = self.env.context.get('active_ids', [])
        link_action = self.env.context.get('link_action', False)

        if model or ids:
            command = Command.link(self.collection_id.id) if link_action else Command.unlink(self.collection_id.id)
            self.env[model].browse(ids).collection_ids = [command]

            self.env['bus.bus']._sendone(self.env.user.partner_id, 'user_menu_collection_items_changed', {})
