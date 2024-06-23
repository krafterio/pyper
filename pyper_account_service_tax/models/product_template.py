# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models, Command


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('detailed_type')
    def _onchange_detailed_type_taxes(self):
        for record in self:
            # Sale
            sale_tax = (self.env.companies.account_sale_tax_id
                        or self.env.companies.root_id.sudo().account_sale_tax_id)
            sale_service_tax = (self.env.companies.account_sale_service_tax_id
                                or self.env.companies.root_id.sudo().account_sale_service_tax_id)

            for tax in record.taxes_id:
                record.taxes_id = [Command.unlink(tax.id)]

            # Sale: Use defined service type
            if 'service' == record.detailed_type and sale_service_tax:
                record.taxes_id = [Command.link(sale_service_tax.id)]

            # Sale: Search service tax equivalent
            elif sale_tax:
                tax_id = sale_tax.id

                if 'service' == record.detailed_type:
                    tax_id = self.env['account.tax'].search([
                        ('active', '=', True),
                        ('amount', '=', sale_tax.amount),
                        ('amount_type', '=', sale_tax.amount_type),
                        ('type_tax_use', '=', sale_tax.type_tax_use),
                        ('price_include', '=', sale_tax.price_include),
                        ('country_id', '=', sale_tax.country_id.id),
                        ('tax_scope', '=', 'service'),
                    ], order='sequence asc, id asc', limit=1).id

                record.taxes_id = [Command.link(tax_id or sale_tax.id)]

            # Purchase
            purchase_tax = (self.env.companies.account_purchase_tax_id
                            or self.env.companies.root_id.sudo().account_purchase_tax_id)
            purchase_service_tax = (self.env.companies.account_purchase_service_tax_id
                                    or self.env.companies.root_id.sudo().account_purchase_service_tax_id)

            for tax in record.supplier_taxes_id:
                record.supplier_taxes_id = [Command.unlink(tax.id)]

            # Purchase: Use defined service type
            if 'service' == record.detailed_type and purchase_service_tax:
                record.supplier_taxes_id = [Command.link(purchase_service_tax.id)]

            # Purchase: Search service tax equivalent
            elif purchase_tax:
                tax_id = purchase_tax.id

                if 'service' == record.detailed_type:
                    tax_id = self.env['account.tax'].search([
                        ('active', '=', True),
                        ('amount', '=', purchase_tax.amount),
                        ('amount_type', '=', purchase_tax.amount_type),
                        ('type_tax_use', '=', purchase_tax.type_tax_use),
                        ('price_include', '=', purchase_tax.price_include),
                        ('country_id', '=', purchase_tax.country_id.id),
                        ('tax_scope', '=', 'service'),
                    ], order='sequence asc, id asc', limit=1).id

                record.supplier_taxes_id = [Command.link(tax_id or purchase_tax.id)]
