# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models
from odoo.tools import ormcache


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

    @ormcache('frozenset(self.env.user.groups_id.ids)', 'tuple(model_field_names)')
    def get_access_rights(self, model_field_names):
        """
        :param model_field_names: The list of tuple defining model name and field name
        """
        model_names = []
        field_names = []

        for model_field_name in model_field_names:
            if model_field_name[0] not in model_names:
                model_names.append(model_field_name[0])

            if model_field_name[1] not in field_names:
                field_names.append(model_field_name[1])

        access_rights = self.env['ir.model.fields.access'].sudo().search([
            ('model_id.model', 'in', model_names),
            ('field_id.name', 'in', field_names),
            ('group_id', 'in', self.env.user.groups_id.ids)
        ])

        map_access_rights = {}
        for access_right in access_rights:
            key = access_right.model_id.model + ':' + access_right.field_id.name
            map_access_rights[key] = self._merge_access_rights(
                self._build_access_right_map(access_right),
                map_access_rights.get(key, None)
            )

        return map_access_rights

    @staticmethod
    def _build_access_right_map(record):
        return {
            'perm_read': record.perm_read,
            'perm_write': record.perm_write,
            'perm_invisible': record.perm_invisible,
        }

    @staticmethod
    def _merge_access_rights(new_access, previous_access):
        if previous_access is None:
            return new_access

        if new_access.get('perm_read', False):
            previous_access.update({'perm_read': True})

        if new_access.get('perm_write', False):
            previous_access.update({'perm_read': True, 'perm_write': True})

        previous_access.update({'perm_invisible': not previous_access.get('perm_read', False)})

        return previous_access
