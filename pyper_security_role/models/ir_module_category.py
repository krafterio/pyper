# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResGroupsPrivilege(models.Model):
    _inherit = 'res.groups.privilege'

    is_role = fields.Boolean(
        string='Is role?',
    )
