# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_note_button = fields.Boolean(
        'Add note button to chatter?',
        config_parameter='pyper_web_theme_activity.show_note_button',
    )

    def set_values(self):
        super().set_values()

        user_group = self.env.ref('base.group_user')
        note_group = self.env.ref('pyper_web_theme_activity.group_can_write_notes')

        if self.env['ir.config_parameter'].sudo().get_param('pyper_web_theme_activity.show_note_button'):
            user_group._apply_group(note_group)
        else:
            user_group._remove_group(note_group)
