# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models


class IrRule(models.AbstractModel):
    _inherit = 'ir.rule'

    @api.model
    def _eval_context(self):
        """Returns a dictionary to use as evaluation context for
           ir.rule domains.
           Note: organization_ids contains the ids of the activated organizations
           by the user with the switch company menu. These organizations are
           filtered and trusted.
        """
        res = super(IrRule, self)._eval_context()
        res.update({
            'organization_ids': self.env.organizations.ids,
            'organization_id': self.env.organization.id,
        })

        return res

    def _compute_domain_keys(self):
        """ Return the list of context keys to use for caching ``_compute_domain``. """
        res = super(IrRule, self)._compute_domain_keys()
        res.append('allowed_organization_ids')

        return res
