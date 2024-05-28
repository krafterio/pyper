# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class Base(models.AbstractModel):
    _inherit = 'base'

    def with_organization(self, organization):
        """ with_organization(organization)

        Return a new version of this recordset with a modified context, such that::

            result.env.organization = organization
            result.env.organizations = self.env.organizations | organization

        :param organization: main organization of the new environment.
        :type organization: :class:`~odoo.addons.pyper_organization.models.Organization` or int

        .. warning::

            When using an unauthorized organization for current user,
            accessing the organization(s) on the environment may trigger
            an AccessError if not done in a sudoed environment.
        """
        if not organization:
            # With organization = None/False/0/[]/empty recordset: keep current environment
            return self

        organization_id = int(organization)
        allowed_organization_ids = self.env.context.get('allowed_organization_ids', [])

        if allowed_organization_ids and organization_id == allowed_organization_ids[0]:
            return self

        # Copy the allowed_organization_ids list
        # to avoid modifying the context of the current environment.
        allowed_organization_ids = list(allowed_organization_ids)

        if organization_id in allowed_organization_ids:
            allowed_organization_ids.remove(organization_id)

        allowed_organization_ids.insert(0, organization_id)

        return self.with_context(allowed_organization_ids=allowed_organization_ids)
