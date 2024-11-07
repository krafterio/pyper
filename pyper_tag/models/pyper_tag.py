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
        index=True,
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
        index=True, 
        help="If checked, this tag will be visible to all users."
    )

    tag_model_name = fields.Char(
        'Associated Model',
        readonly=True,
        required=True,
        index=True,
    )

    family_id = fields.Many2one(
        'pyper.tag.family', 
        string="Tag family", 
        help="The family to which this tag belongs"
    )

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

    @api.constrains('is_public', 'family_id')
    def _check_family_has_same_visibility(self):
        for pyper_tag in self:
            if pyper_tag.family_id and pyper_tag.family_id.is_public is not self.is_public:
                raise ValidationError(_('A tag and his family must have the same visibility, both public either private'))


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

    @api.depends('emoji', 'name', 'is_public', 'family_id')
    def _compute_display_name(self):
        for pyper_tag in self:
            name_list = []
            # [+] Improve this in display related flow
            # if pyper_tag.family_id:
            #     name_list.append(f'[{pyper_tag.family_id.display_name}]')
            if pyper_tag.emoji:
                name_list.append(pyper_tag.emoji)
            if pyper_tag.name:
                name_list.append(pyper_tag.name)
            name_string = ' '.join(name_list)
            if not pyper_tag.is_public:
                name_string = '(' + name_string + ')'
            pyper_tag.display_name = name_string
               
