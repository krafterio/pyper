# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from odoo.exceptions import UserError
import requests

class ResPartner(models.Model):
    _inherit = 'res.partner'

    linkedin_url = fields.Char(
        'Linkedin url'
    )

    company_linkedin_url = fields.Char(
        'Company LinkedIn Url',
    )