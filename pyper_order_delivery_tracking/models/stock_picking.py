# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# from odoo import models, api
#
#
# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#
#
#     @api.depends('sale_id', 'sale_id.carrier_tracking_ref', 'sale_id.carrier_id')
#     def _compute_carrier_tracking(self):
#