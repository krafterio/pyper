# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    carrier_tracking_ref = fields.Char(string='Tracking number')
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier')
    several_picking_ids = fields.Boolean(compute='_compute_several_picking_ids')
    picking_ref = fields.Char(related='picking_ids.name')
    picking_state = fields.Selection(related='picking_ids.state')
    move_ids = fields.One2many(related='picking_ids.move_ids')
    
    def _compute_several_picking_ids(self):
        for order in self:
            order.several_picking_ids = len(order.picking_ids) > 1
    
    def button_validate(self):
        self.picking_ids.button_validate()

    @api.onchange('carrier_tracking_ref', 'carrier_id')
    def _onchange_tracking(self):
        for order in self:
            if len(order.picking_ids) > 1:
                raise UserError(_('You are entering a tracking number (supposed to be unique) when you have made two deliveries.\n'
                                  'Please enter this informations on the dedicated page, by clicking on the “Delivery” button at the top.'))
            picking_ids = self.env['stock.picking'].browse(order.picking_ids.ids)
            for picking in picking_ids:
                picking.carrier_tracking_ref = order.carrier_tracking_ref
                picking.carrier_id = order.carrier_id
