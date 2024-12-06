# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models
from odoo.tools import image_data_uri


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        user = self.env.user

        for company in user.company_ids:
            logo_data = image_data_uri(company.logo_web) if company.logo_web else False
            company_vals = {
                'logo_data': logo_data,
                'initials': company.initials,
            }

            if company.id in result['user_companies']['allowed_companies']:
                result['user_companies']['allowed_companies'][company.id].update(company_vals)

            if company.id in result['user_companies']['disallowed_ancestor_companies']:
                result['user_companies']['disallowed_ancestor_companies'][company.id].update(company_vals)

        return result
