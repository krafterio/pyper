# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class PyperTag(models.Model):
    _name = 'pyper.tag'
    _description = 'Generic Tag Model'

    # [!] La valeur, ce qui est écrit sur le tag : "Flow en meeting", "Prospect à relancer avant mai"
    name = fields.Char(
        'Tag name',
        required=True,
    )

    display_name = fields.Char(
        string="Displayed tag name", 
        compute="_compute_display_name",
        store=True
    )

    tag_model_name = fields.Char(
        'Associated Model',
        # default=lambda self: self.env.context.get('default_tag_model_name')
    )

    # [!] PyperTag design related properties
    # [+] Affiner les champs nécessaires et créer d'autres classes séparées si nécessaire
    color_id = fields.Many2one(
        'pyper.tag.color',
        string='Color'
    )

    color_name = fields.Char(
        'Color name',
        related='color_id.name',
        # store=True,
        # readonly=True
    )

    color_hex_code = fields.Char(
        string='Color Hex code',
        related='color_id.hex_code',
        store=True,
        # readonly=True
    )

    emoji = fields.Char(
        'Emoji',
        help="Emoji representing the tag"
     )

    _sql_constraints = [
        ('unique_model_value', 'unique(name, tag_model_name)',
         'Each tag name must be unique for a given model'),
    ]

    @api.depends('emoji', 'name')
    def _compute_display_name(self):
        for pyper_tag in self:
            emoji = pyper_tag.emoji or ""
            name = pyper_tag.name or ""
            pyper_tag.display_name = f"{emoji} {name}" if emoji else name


    @api.model_create_multi
    def create(self, vals_list):
        print("Here in PyperTag model")
        return super(PyperTag, self).create(vals_list)

    def write(self, vals):
        # if 'tag_ids' in vals:
        print("Here in write PyperTag model")
        # for tag in self.tag_ids:
        #     tag.tag_model_name = self._name

        return super().write(vals)
