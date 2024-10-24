# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class PyperTag(models.Model):
    _name = 'pyper.tag'
    _description = 'Generic Tag Model'

    # [!] Comment sera nommé l'objet en lui même : un tag / un onglet / une marque ... choisi par l'utilisateur
    generic_name = fields.Char(
        'Generic name',
        required=True,
        default='Tag'
    )

    # [!] La valeur, ce qui est écrit sur le tag : "Flow en meeting", "Prospect à relancer avant mai"
    value = fields.Char(
        'Value',
        required=True,
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
        # store=True,
        # readonly=True
    )

    icon = fields.Char('Icon')
