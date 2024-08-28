# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models
from odoo.tools import ormcache, frozendict


class IrModelFieldsAccess(models.Model):
    _name = 'ir.model.fields.access'
    _description = 'Field access right'
    _order = 'model_id ASC, field_id ASC'

    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        related='field_id.model_id',
        store=True,
    )

    field_id = fields.Many2one(
        'ir.model.fields',
        'Field',
        ondelete='cascade',
        required=True,
    )

    model_name = fields.Char(
        string='Model name',
        related='model_id.model',
        store=True,
    )

    field_name = fields.Char(
        string='Field name',
        related='field_id.name',
        store=True,
    )

    group_id = fields.Many2one(
        'res.groups',
        string="Security group",
        required=True,
    )

    perm_read = fields.Boolean(
        string='Read',
        default=False,
    )

    perm_write = fields.Boolean(
        string='Edit',
        default=False,
    )

    perm_invisible = fields.Boolean(
        string='Invisible',
        compute='_compute_perm_invisible',
        store=True,
    )

    @api.depends('perm_read', 'perm_write')
    def _compute_perm_invisible(self):
        for rec in self:
            rec.perm_invisible = not rec.perm_read

    @api.onchange('perm_write')
    def _onchange_perm_edit(self):
        for rec in self:
            if not rec.perm_read and rec.perm_write:
                rec.perm_read = True

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self.env.registry.clear_cache('default')

        return res

    def write(self, vals):
        res = super().write(vals)
        self.env.registry.clear_cache('default')

        return res

    def unlink(self):
        res = super().unlink()
        self.env.registry.clear_cache('default')

        return res

    @api.onchange('perm_read')
    def _onchange_perm_read(self):
        for rec in self:
            if not rec.perm_read and rec.perm_write:
                rec.perm_write = False

    def check_field_access_right(self, model: str, field: str, operation: str) -> bool:
        if operation not in ['read', 'write']:
            return False

        if self.env.su:
            return True

        return self.get_field_access_rights(model, field).get(operation, True)

    def get_field_access_rights(self, model: str, field: str) -> dict:
        return self.get_access_rights().get(model, {}).get(field, frozendict(build_access_right_item()))

    @ormcache('frozenset(self.env.user.groups_id.ids)')
    def get_access_rights(self):
        domain = [('group_id', 'in', self.env.user.groups_id.ids)]
        field_names = ['model_name', 'field_name', 'perm_read', 'perm_write', 'perm_invisible']
        access_rights = self.env['ir.model.fields.access'].sudo().search_read(domain, field_names)
        map_access_rights = {}

        for access_right in access_rights:
            model_name = access_right.get('model_name')
            field_name = access_right.get('field_name')

            if model_name not in map_access_rights:
                map_access_rights[model_name] = {}

            map_access_rights[model_name][field_name] = merge_access_rights(
                build_access_right_map(access_right),
                map_access_rights[model_name].get(field_name, None),
            )

        return frozendict(map_access_rights)


def build_access_right_map(record):
    return build_access_right_item(
        read=record.get('perm_read', False),
        write=record.get('perm_write', False),
    )


def merge_access_rights(new_access, previous_access):
    if previous_access is None:
        return new_access

    if new_access.get('read', False):
        previous_access.update({'read': True})

    if new_access.get('write', False):
        previous_access.update({'read': True, 'write': True})

    return previous_access


def build_access_right_item(read: bool = True, write: bool = True):
    return {
        'read': read,
        'write': write,
    }
