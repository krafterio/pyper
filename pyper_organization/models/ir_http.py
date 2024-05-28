# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models
from odoo.tools import image_data_uri


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        user = self.env.user

        result.update({
            'user_organizations': {
                'current_organization': user.organization_id.id,
                'allowed_organizations': {
                    organization.id: {
                        'id': organization.id,
                        'name': organization.name,
                        'initials': organization.initials,
                        'sequence': organization.sequence,
                        'company_id': organization.company_id.id,
                        'logo_data': image_data_uri(organization.logo_web) if organization.logo_web else False,
                    } for organization in user.organization_ids
                },
            }
        })

        return result
