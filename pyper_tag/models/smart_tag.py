# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, AccessError


class SmartTag(models.Model):
    _name = 'smart.tag'
    _description = 'Generic Tag Model'
    _order='is_public DESC, family_id, name'

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
        index=True,
    )

    family_id = fields.Many2one(
        'smart.tag.family', 
        string="Tag family", 
        help="The family to which this tag belongs"
    )

    color_id = fields.Char('Tag color')

    emoji = fields.Selection(
        selection=[
            ('✅', '✅'),   ('❌', '❌'),   ('🌟', '🌟'),   ('⚡', '⚡'),
            ('🔥', '🔥'),   ('💧', '💧'),   ('🔔', '🔔'),   ('🚀', '🚀'),
            ('📅', '📅'),   ('📈', '📈'),   ('🎯', '🎯'),   ('🚧', '🚧'),
            ('🛠️', '🛠️'),   ('🍪', '🍪'),   ('🌊', '🌊'),   ('🛕', '🛕'),
            ('🌙', '🌙'),   ('⭐', '⭐'),   ('☀️',   '☀️'),   ('🐼', '🐼'),
            ('🐱', '🐱'),   ('🐘', '🐘'),   ('🐧', '🐧'),   ('🐷', '🐷'),
            ('🐞', '🐞'),   ('🐢', '🐢'),   ('🐙', '🐙'),   ('🐳', '🐳'),
            ('🎉', '🎉'),   ('💡', '💡'),   ('🎵', '🎵'),   ('🖋️', '🖋️'),
            ('🎨', '🎨'),   ('🎓', '🎓'),   ('🚴', '🚴'),   ('📚', '📚'),
            ('🏆', '🏆'),   ('🎁', '🎁'),   ('💼', '💼'),   ('🛡️', '🛡️'),
            ('🔑', '🔑'),   ('📌', '📌'),   ('📎', '📎'),   ('🧩', '🧩'),
            ('🔍', '🔍'),   ('🧱', '🧱'),   ('📜', '📜'),   ('🛒', '🛒'),
            ('🧹', '🧹'),   ('📦', '📦'),   ('🗂️', '🗂️'),   ('🚦', '🚦'),
            ('🗺️', '🗺️'),   ('🎬', '🎬'),   ('🎮', '🎮'),   ('🎲', '🎲'),
            ('🔋', '🔋'),   ('🌍', '🌍'),   ('🌈', '🌈'),   ('🌻', '🌻'),
               
            ('😀', '😀'),   ('😁', '😁'),   ('😂', '😂'),   ('🤣', '🤣'),
            ('😊', '😊'),   ('😇', '😇'),   ('🙂', '🙂'),   ('🙃', '🙃'),
            ('😉', '😉'),   ('😌', '😌'),   ('😍', '😍'),   ('😘', '😘'),
            ('😗', '😗'),   ('😋', '😋'),   ('😜', '😜'),   ('🤪', '🤪'),
            ('😎', '😎'),   ('🥳', '🥳'),   ('🤩', '🤩'),   ('🥺', '🥺'),
            ('😢', '😢'),   ('😭', '😭'),   ('😤', '😤'),   ('😠', '😠'),
            ('😡', '😡'),   ('🤬', '🤬'),   ('🤯', '🤯'),   ('😱', '😱'),
            ('😨', '😨'),   ('😰', '😰'),   ('😥', '😥'),   ('😓', '😓'),
            ('🤮', '🤮'),   ('🧟', '🧟'),

            ('🍎', '🍎'),   ('🍇', '🍇'),   ('🍌', '🍌'),   ('🍉', '🍉'),
            ('🍓', '🍓'),   ('🍒', '🍒'),   ('🍍', '🍍'),   ('🥭', '🥭'),
            ('🍑', '🍑'),   ('🥝', '🥝'),   ('🍋', '🍋'),   ('🍊', '🍊'),
            ('🥑', '🥑'),   ('🥦', '🥦'),   ('🥕', '🥕'),   ('🌽', '🌽'),
            ('🍔', '🍔'),   ('🍕', '🍕'),   ('🍟', '🍟'),   ('🌭', '🌭'),
            ('🍿', '🍿'),   ('🥗', '🥗'),   ('🍣', '🍣'),   ('🍤', '🍤'),
            ('🍪', '🍪'),   ('🍩', '🍩'),   ('🎂', '🎂'),   ('🍫', '🍫'),
            ('🍭', '🍭'),   ('🍮', '🍮'),   ('🍯', '🍯'),   ('🧁', '🧁'),

            ('🏀', '🏀'),   ('🏐', '🏐'),   ('🎾', '🎾'),   ('🏓', '🏓'),
            ('🥋', '🥋'),   ('🎯', '🎯'),   ('🏹', '🏹'),   ('🛹', '🛹'),
            ('🚗', '🚗'),   ('🚕', '🚕'),   ('🚙', '🚙'),   ('🚂', '🚂'),
            ('🚢', '🚢'),   ('🚁', '🚁'),   ('🚶', '🚶'),   ('🌵', '🌵'),
            ('⚽', '⚽'),   ('🌴', '🌴'),   ('🌳', '🌳'),   ('🌲', '🌲'),
            ('🌿', '🌿'),   ('☘️',   '☘️'),   ('🍀', '🍀'),   ('🍃', '🍃'),
            ('🍂', '🍂'),   ('🍁', '🍁'),   ('🌾', '🌾'),   ('💐', '💐'),
            ('🌸', '🌸'),   ('🌺', '🌺'),   ('🌼', '🌼'),   ('🌷', '🌷'),
            ('🌹', '🌹'),   ('🥀', '🥀'),   ('🌻', '🌻'),   ('🪷', '🪷'),
            ('🪴', '🪴'),   ('🌱', '🌱'),   ('🪹', '🪹'),   ('🪵', '🪵'),
        ],
        string="Emoji",
    )

    @api.constrains('is_public', 'family_id')
    def _check_family_has_same_visibility(self):
        for smart_tag in self:
            if smart_tag.family_id and smart_tag.family_id.is_public is not self.is_public:
                raise ValidationError(_('A tag and his family must have the same visibility, both public either private'))


    @api.constrains('name', 'tag_model_name', 'is_public')
    def _check_unique_tag_name_per_model(self):
        for smart_tag in self:
            check_method = self._check_unique_public_tag_name_per_model if smart_tag.is_public else self._check_unique_private_tag_name_per_model
            check_method(smart_tag)

    def _check_unique_public_tag_name_per_model(self, smart_tag):
        for smart_tag in self:
            domain = [
            ('name', '=', smart_tag.name),
            ('tag_model_name', '=', smart_tag.tag_model_name),
            ('is_public', '=', True),
            ('id', '!=', smart_tag.id),
        ]
        if self.search_count(domain) > 0:
            raise ValidationError(_('A public tag with this name already exists for the selected model.'))
                 
    def _check_unique_private_tag_name_per_model(self, smart_tag):
        for smart_tag in self:
            domain = [
                ('name', '=', smart_tag.name),
                ('tag_model_name', '=', smart_tag.tag_model_name),
                ('is_public', '=', False),
                ('user_id', '=', smart_tag.user_id.id),
                ('id', '!=', smart_tag.id),
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('You already have a private tag with this name.'))

    @api.depends('emoji', 'name', 'is_public', 'family_id.display_name')
    def _compute_display_name(self):
        for smart_tag in self:
            name_list = []
            if smart_tag.family_id:
                name_list.append(smart_tag.family_id.display_name)
                name_list.append('\u00B7') # middle dot
            if smart_tag.emoji:
                name_list.append(smart_tag.emoji)
            if smart_tag.name:
                name_list.append(smart_tag.name)
            name_string = ' '.join(name_list)
            if not smart_tag.is_public:
                name_string = '(' + name_string + ')'
            smart_tag.display_name = name_string


    def action_open_tag_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'smart.tag',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_public') and not self.env.user.has_group('base.group_system'):
                raise AccessError(_('Only administrators can create public tags.'))
        return super(SmartTag, self).create(vals_list)

    def write(self, vals):
        for smart_tag in self:
            if smart_tag.is_public and not self.env.user.has_group('base.group_system'):
                raise AccessError(_('Only administrators can edit a public tag.'))
        return super(SmartTag, self).write(vals)

    def unlink(self):
        for smart_tag in self:
            if smart_tag.is_public and not self.env.user.has_group('base.group_system'):
                raise AccessError(_('Only administrators can delete public tags.'))
        return super(SmartTag, self).unlink()
               
