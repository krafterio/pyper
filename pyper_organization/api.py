# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, tools, _
from odoo.exceptions import AccessError


class Environment(api.Environment):
    @tools.lazy_property
    def organization(self):
        """Return the current organization (as an instance).

        If not specified in the context (`allowed_organization_ids`),
        fallback on current user main organization.

        :raise AccessError: invalid or unauthorized `allowed_organization_ids` context key content.
        :return: current organization (default=`self.user.organization_id`), with the current environment
        :type organization: :class:`~odoo.addons.pyper_organization.models.Organization`

        .. warning::

            No sanity checks applied in sudo mode!
            When in sudo mode, a user can access any organization,
            even if not in his allowed companies.

            This allows to trigger inter-organization modifications,
            even if the current user doesn't have access to
            the targeted organization.
        """
        organization_ids = self.context.get('allowed_organization_ids', [])

        if organization_ids:
            if not self.su:
                user_organization_ids = self.user._get_organization_ids()

                if set(organization_ids) - set(user_organization_ids):
                    raise AccessError(_('Access to unauthorized or invalid organizations.'))

            return self['organization'].browse(organization_ids[0])

        return self.user.organization_id.with_env(self)

    @tools.lazy_property
    def organizations(self):
        """Return a recordset of the enabled organizations by the user.

        If not specified in the context(`allowed_organization_ids`),
        fallback on current user organizations.

        :raise AccessError: invalid or unauthorized `allowed_organization_ids` context key content.
        :return: current organizations (default=`self.user.organization_ids`), with the current environment
        :type organization: :class:`~odoo.addons.pyper_organization.models.Organization`

        .. warning::

            No sanity checks applied in sudo mode !
            When in sudo mode, a user can access any organization,
            even if not in his allowed organizations.

            This allows to trigger inter-organization modifications,
            even if the current user doesn't have access to
            the targeted organization.
        """
        organization_ids = self.context.get('allowed_organization_ids', [])
        user_organization_ids = self.user._get_organization_ids()

        if organization_ids:
            if not self.su:
                if set(organization_ids) - set(user_organization_ids):
                    raise AccessError(_('Access to unauthorized or invalid organizations.'))

            return self['organization'].browse(organization_ids)

        # By setting the default organizations to all user organizations instead of the main one
        # we save a lot of potential trouble in all "out of context" calls, such as
        # /mail/redirect or /web/image, etc. And it is not unsafe because the user does
        # have access to these other organizations. The risk of exposing foreign records
        # (wrt to the context) is low because all normal RPCs will have a proper
        # allowed_organization_ids.
        # Examples:
        #   - when printing a report for several records from several organizations
        #   - when accessing to a record from the notification email template
        #   - when loading an binary image on a template
        return self['organization'].browse(user_organization_ids)


api.Environment = Environment
