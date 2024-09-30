# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    drop_contact_batch_id = fields.Many2one(
        'res.partner.drop_contact.batch',
        'Drop contact batch',
    )

    drop_contact_batch_state = fields.Selection(
        string='Drop contact state',
        related='drop_contact_batch_id.state',
    )

    def action_enrich_contact_info(self):
        if len(self.ids) > 250 or len(self.ids) == 0:
            raise UserError(_('The action to enrich contact info can accept only 250 contacts by batch'))

        for partner in self:
            if partner.is_company:
                raise UserError(_('The action to enrich contact info can accept only individual partner'))

        self.env['res.partner.drop_contact.batch'].create({
            'partner_ids': self.ids,
        }).with_delay().retrieve_info().process_one()
