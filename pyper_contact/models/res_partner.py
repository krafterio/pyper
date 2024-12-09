# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_user = fields.Boolean(
        'Is user',
        compute="_compute_is_user",
        store=True,
    )

    @api.depends('user_ids')
    def _compute_is_user(self):
        for partner in self:
            partner.is_user = len(partner.user_ids) > 0


    @api.onchange('phone', 'country_id', 'company_id')
    def _onchange_phone_validation(self):
        for contact in self:
            if contact.phone:
                if len(contact.phone) == 10 and contact.phone.isdigit():
                    contact.phone = contact._display_a_ten_digit_phone(contact.phone)
                else:
                    super(ResPartner, self)._onchange_phone_validation() 


    @api.onchange('mobile', 'country_id', 'company_id')
    def _onchange_mobile_validation(self):
        for contact in self:
            if contact.mobile:
                if len(contact.mobile) == 10 and contact.mobile.isdigit():
                    contact.mobile = contact._display_a_ten_digit_phone(contact.mobile)
                else:
                    super(ResPartner, self)._onchange_mobile_validation() 


    def _display_a_ten_digit_phone(self, phone):
        return f'{phone[:2]} {phone[2:4]} {phone[4:6]} {phone[6:8]} {phone[8:]}'


    