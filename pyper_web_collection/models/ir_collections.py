# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, Command

from random import randint


class IrCollections(models.Model):
    _name = 'ir.collections'
    _description = 'Collections'
    _order = 'category asc, sequence asc'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )

    active = fields.Boolean(
        'Active',
        default=True,
    )

    system = fields.Boolean(
        'Is system?',
        default=False,
    )

    category = fields.Selection(
        [
            ('system', 'System'),
            ('personal', 'Personal'),
            ('shared', 'Shared'),
        ],
        store=True,
        compute='_compute_category',
    )

    sequence = fields.Integer(
        'Sequence',
        default=lambda self: (self.search([], order='sequence desc', limit=1).sequence or 0) + 1,
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        ondelete='cascade',
        default=lambda self: self.env.user.id,
        required=True,
    )

    shared = fields.Boolean(
        'Collection shared',
        compute='_compute_shared',
        inverse='_inverse_shared',
        store=True,
    )

    shared_user_ids = fields.Many2many(
        'res.users',
        'ir_collections_shared_user_rel',
        'collection_id',
        'user_id',
        string='Users',
        help="if this field is empty, the collection applies to all users. Otherwise, the collection applies to only selected users.",
    )

    shared_user_ids_field_domain = fields.Binary(
        compute='_compute_shared_user_ids_field_domain',
    )

    group_ids = fields.Many2many(
        'res.groups',
        'ir_collections_group_rel',
        'ir_collection_id',
        'group_id',
        string='Groups',
        help="If this field is empty, the collection applies to all users. Otherwise, the collection applies to the users of those groups only.",
    )

    res_model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        domain=[('is_collectionable', '=', True), ('transient', '=', False)],
    )

    res_model_name = fields.Char(
        string='Model name',
        compute='_compute_res_model_name',
        inverse='_inverse_res_model_name',
        store=True,
    )

    ir_action_id = fields.Many2one(
        'ir.actions.act_window',
        string='Action',
        ondelete='cascade',
        required=True,
    )

    ir_action_id_field_domain = fields.Binary(
        compute='_compute_ir_action_id_field_domain',
    )

    menu_ir_action_id = fields.Many2one(
        'ir.actions.act_window',
        string='Menu Action',
        ondelete='cascade',
        readonly=True,
        help='The dedication action of collection',
    )

    menu_id = fields.Many2one(
        'ir.ui.menu',
        string='Menu item',
        readonly=True,
        ondelete='cascade',
    )

    display_counter = fields.Boolean(
        'Display Counter',
        default=True,
        help='Allow to display a counter on menu item',
    )

    font_icon = fields.Char('Font icon')

    font_icon_color = fields.Char('Font icon color')

    def _get_default_color(self):
        return randint(1, 11)

    color = fields.Integer(
        string='Color',
        default=_get_default_color,
    )

    @api.model
    def get_menu_action_vals(self):
        self.ensure_one()
        action = self.ir_action_id.sudo()

        return {
            'name': self.name,
            'res_model': action.res_model,
            'target': action.target,
            'view_mode': action.view_mode,
            'mobile_view_mode': action.mobile_view_mode,
            'view_id': action.view_id.id,
            'search_view_id': action.search_view_id.id,
            'help': action.help,
            'domain': [('collection_ids', '=', self.id)],
            'context': action.context,
            'limit': action.limit,
            'ir_collections_id': self.id,
            'view_ids': [Command.clear(), *[Command.link(u.id) for u in action.view_ids]],
        }

    @api.model
    def get_menu_vals(self):
        self.ensure_one()
        action = self.menu_ir_action_id.sudo()

        return {
            'name': self.name,
            'sequence': self.sequence,
            'action': str(action.type) + ',' + str(action.id),
            'display_counter': self.display_counter,
            'font_icon': self.font_icon or self._get_default_font_icon(),
            'font_icon_color': self.font_icon_color,
            'category_id': self.env.ref('pyper_web_collection.menu_category_shared_collections').id
                if self.shared
                else self.env.ref('pyper_web_collection.menu_category_my_collections').id,
            'collection_id': self.id,
            'user_id': self.env.user.id,
            'shared_user_ids': [Command.clear(), *[Command.link(u.id) for u in self.shared_user_ids]],
            'groups_id': [Command.clear(), *[Command.link(g.id) for g in self.group_ids]],
        }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_shared()
        records._sync_menu_ir_action()
        records._sync_ir_ui_menu()

        return records

    def write(self, vals):
        res = super().write(vals)
        self._sync_shared()
        self._sync_menu_ir_action()
        self._sync_ir_ui_menu()

        return res

    def unlink(self):
        sudo = self.sudo()
        sudo.menu_id.sudo().unlink()

        return super(IrCollections, sudo).unlink()

    def _sync_shared(self):
        for record in self:
            if record.shared and len(record.shared_user_ids) == 0 and len(record.group_ids) == 0:
                record.shared = False

    def _sync_menu_ir_action(self):
        for record in self:
            if record.menu_ir_action_id:
                record.menu_ir_action_id.sudo().write(record.get_menu_action_vals())
            else:
                record.menu_ir_action_id = self.env['ir.actions.act_window'].sudo().create(record.get_menu_action_vals())

    def _sync_ir_ui_menu(self):
        for record in self:
            if record.sudo().menu_id:
                record.sudo().menu_id.write(record.get_menu_vals())
            else:
                record.menu_id = self.env['ir.ui.menu'].sudo().create(record.get_menu_vals())

    @api.depends('shared_user_ids', 'group_ids')
    def _compute_shared(self):
        for record in self:
            record.shared = len(record.shared_user_ids) > 0 or len(record.group_ids) > 0

    @api.onchange('shared')
    def _inverse_shared(self):
        for record in self:
            if not record.shared:
                record.shared_user_ids = [Command.clear()]
                record.group_ids = [Command.clear()]

    @api.onchange('res_model_name')
    def _onchange_res_model_id(self):
        default_model_name = self.env.context.get('default_res_model_name', False)
        default_ir_action_id = self.env.context.get('default_ir_action_id', False)

        for record in self:
            if record.res_model_id:
                domain = [
                    ('res_model', '=', record.res_model_name),
                    ('ir_collections_id', '=', False),
                ]
                fallback_domain = [*domain]

                # Select default action only if action is not an action for collection
                if record.res_model_name == default_model_name and default_ir_action_id:
                    domain.append(('id', '=', default_ir_action_id))

                record.ir_action_id = self.env['ir.actions.act_window'].search(domain, limit=1)

                if not record.ir_action_id:
                    record.ir_action_id = self.env['ir.actions.act_window'].search(fallback_domain, limit=1)
            else:
                record.ir_action_id = False

    @api.onchange('user_id')
    def _onchange_user_id(self):
        for record in self:
            if record.user_id:
                record.shared_user_ids = [Command.unlink(record.user_id.id)]

    @api.depends('system', 'shared')
    def _compute_category(self):
        for record in self:
            if record.system:
                record.category = 'system'
            elif record.shared:
                record.category = 'shared'
            else:
                record.category = 'personal'

    @api.depends('res_model_id')
    def _compute_res_model_name(self):
        for record in self:
            record.res_model_name = record.res_model_id.model

    @api.onchange('res_model_name')
    def _inverse_res_model_name(self):
        for record in self:
            if record.res_model_name and not record.res_model_id:
                record.res_model_id = record.res_model_id.search([('model', '=', self.res_model_name)], limit=1)
                record.res_model_name = record.res_model_id.model

    @api.depends('user_id')
    def _compute_shared_user_ids_field_domain(self):
        for record in self:
            record.shared_user_ids_field_domain = [('id', '!=', record.user_id.id)]

    @api.depends('res_model_name')
    def _compute_ir_action_id_field_domain(self):
        for record in self:
            record.ir_action_id_field_domain = [('res_model', '=', self.res_model_name), ('ir_collections_id', '=', False)]

    def _get_default_font_icon(self):
        return 'fa fa-database'
