# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


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

    user_id = fields.Many2one(
        'res.users', 
        string="Created By", 
        default=lambda self: self.env.user,
        readonly=True
    )

    is_public = fields.Boolean(
        string="Is Public", 
        default=False, 
        help="If checked, this tag will be visible to all users."
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
            ('🌊', '🌊'),
            ('🌿', '🌿'),
            ('⚡', '⚡'),
            ('🐼', '🐼'),
            ('🐱', '🐱'),
            ('🐘', '🐘'),
            ('🐧', '🐧'),
            ('🐷', '🐷'),
            ('🐞', '🐞'),
            ('🐢', '🐢'),
            ('🐙', '🐙'),
            ('🐳', '🐳'),
        ],
        string="Emoji",
    )

    @api.constrains('name', 'tag_model_name', 'is_public')
    def _check_unique_tag_name_per_model(self):
        for pyper_tag in self:
            check_method = self._check_unique_public_tag_name_per_model if pyper_tag.is_public else self._check_unique_private_tag_name_per_model
            check_method(pyper_tag)

    def _check_unique_public_tag_name_per_model(self, pyper_tag):
        for pyper_tag in self:
            domain = [
            ('name', '=', pyper_tag.name),
            ('tag_model_name', '=', pyper_tag.tag_model_name),
            ('is_public', '=', True),
            ('id', '!=', pyper_tag.id),
        ]
        if self.search_count(domain) > 0:
            raise ValidationError(_('A public tag with this name already exists for the selected model.'))
                 
    def _check_unique_private_tag_name_per_model(self, pyper_tag):
        for pyper_tag in self:
            domain = [
                ('name', '=', pyper_tag.name),
                ('tag_model_name', '=', pyper_tag.tag_model_name),
                ('is_public', '=', False),
                ('user_id', '=', pyper_tag.user_id.id),
                ('id', '!=', pyper_tag.id),
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('You already have a private tag with this name.'))

    @api.depends('emoji', 'name')
    def _compute_display_name(self):
        for pyper_tag in self:
            emoji = pyper_tag.emoji or ''
            name = pyper_tag.name or ''
            if pyper_tag.is_public:
                pyper_tag.display_name = f'{emoji} {name}' if emoji else name
            else:
                pyper_tag.display_name = f'({emoji} {name})' if emoji else f'({name})'
