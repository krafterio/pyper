# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    template_attachment_id = fields.Many2one(
        'ir.attachment', 
        string='Conditions Générales', 
        domain=[('mimetype', '=', 'application/pdf')], 
        help="Select a template to attach to the end of the report."
    )
