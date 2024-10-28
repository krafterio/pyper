# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class PyperTag(models.Model):
    _name = 'pyper.tag'
    _description = 'Generic Tag Model'

    name = fields.Char(
        'Tag name',
        required=True,
    )

    display_name = fields.Char(
        'Displayed tag name', 
        compute='_compute_display_name',
        store=True
    )

    

    tag_model_name = fields.Char('Associated Model')

    color_id = fields.Char('Tag color')

    emoji = fields.Selection(
        selection=[
            ('🌟', '🌟'),
            ('✅', '✅'),
            ('❌', '❌'),
            ('🔔', '🔔'),
            ('🛠️', '🛠️'),
            ('📅', '📅'),
            ('📈', '📈'),
            ('🚀', '🚀'),
            ('🎯', '🎯'),
            ('🚧', '🚧'),
            ('🔥', '🔥'),
            ('💧', '💧'),
            ('🍪', '🍪'),
            ('🔥', '🔥'),
            ('🌊', '🌊'),
        ],
        string="Emoji",
    )

    _sql_constraints = [
        ('unique_model_value', 'unique(name, tag_model_name)',
         'Each tag name must be unique for a given model'),
    ]

    @api.depends('emoji', 'name')
    def _compute_display_name(self):
        for pyper_tag in self:
            emoji = pyper_tag.emoji or ''
            name = pyper_tag.name or ''
            pyper_tag.display_name = f'{emoji} {name}' if emoji else name
