# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class PyperTag(models.Model):
    _name = 'pyper.tag'
    _description = 'Generic Tag Model'

    # [!] Comment sera nommé l'objet en lui même : un tag / un onglet / une marque ... choisi par l'utilisateur
    # [!] Utiliser une relation ?
    generic_name = fields.Char(
        'Generic name',
        required=True,
        readonly=True,
        default='Tag' # [!] compute avec le model name ?
    )

    # [!] Le nom du modèle qui hérite du tag, pour que chaque tag soit unique par modèle
    # [!] Pour le moment je n'ai réussi à placer cette valeur que dans le contexte du field du form du test-model
    # [!] Comment automatiser simplement ?
    model_name = fields.Char(
        'Associated Model Name',
        required=True,
        readonly=True,
        default='pyper.tag.default', # [!] to compute test only ?
        help="The model name associated with the tag"
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
        store=True,
        # readonly=True
    )

    icon = fields.Char('Icon')

    _sql_constraints = [
        ('unique_model_value', 'unique(value, model_name)',
         'Each tag value must be unique for a given model'),
    ]


    @api.model_create_multi
    def create(self, vals_list):
        print("Here in PyperTag model")
        print("Parent name= ", self._parent_name)
        return super(PyperTag, self).create(vals_list)

    def write(self, vals):
        # if 'tag_ids' in vals:
        for tag in self.tag_ids:
            tag.model_name = self._name

        return super().write(vals)
