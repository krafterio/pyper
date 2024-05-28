# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import base64

from odoo import api, fields, models, tools, Command, _
from odoo.exceptions import ValidationError


class Organization(models.Model):
    _name = 'organization'
    _description = 'Organization'
    _order = 'sequence ASC'
    _inherit = ['image.mixin']

    active = fields.Boolean(
        default=True,
    )

    sequence = fields.Integer(
        help='Used to order Organizations in the organization switcher',
        default=lambda self: (self.search([], order='sequence desc', limit=1).sequence or 0) + 1,
    )

    name = fields.Char(
        'Name',
        required=True,
    )

    initials = fields.Char(
        'Initials',
        compute='_compute_initials',
    )

    logo_web = fields.Binary(
        compute='_compute_logo_web',
        store=True, attachment=False,
    )

    company_id = fields.Many2one(
        'res.company',
        'Company',
        index=True,
        default=lambda self: self.env.company,
    )

    user_ids = fields.Many2many(
        'res.users',
        'organization_users_rel',
        'oid',
        'user_id',
        string='Users',
    )

    users_count = fields.Integer(
        compute='_compute_users_count',
        string="Number of users",
    )

    @api.depends('name')
    def _compute_initials(self):
        for record in self:
            if record.name:
                record.initials = record.name[0:1].upper()
            else:
                record.initials = '?'

    @api.depends('company_id')
    def _compute_users_count(self):
        for record in self:
            record.users_count = len(record.user_ids)

    @api.depends('image_1920')
    def _compute_logo_web(self):
        for record in self:
            img = record.image_1920
            record.logo_web = img and base64.b64encode(tools.image_process(base64.b64decode(img), size=(180, 0)))

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get('user_ids'):
                values.update({
                    'user_ids': [Command.link(self.env.user.id)],
                })

        organizations = super().create(vals_list)

        self._create_or_update_sequences(organizations)

        return organizations

    def write(self, vals):
        res = super().write(vals)

        for record in self:
            if not record.user_ids:
                raise ValidationError(_('You cannot remove the last associated user'))

        self._create_or_update_sequences(self)

        return res

    def _create_or_update_sequences(self, organizations):
        """ Create or update existing sequence for Organization.
        """
        pass
