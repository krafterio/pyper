# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
import requests
import base64
from datetime import datetime

from odoo.exceptions import UserError


class IcecatForm(models.TransientModel):
    _name = 'icecat.form'
    _description = 'Icecat Form'

    ean_upc = fields.Char(
        'EAN/UPC',
        required=True,
    )

    language_id = fields.Many2one(
        'res.lang',
        'Language',
        required=True,
    )

    detailed_type = fields.Selection(
        [
            ('consu', 'Consumable'),
            ('service', 'Service'),
            ('product', 'Product'),
        ],
        default='product',
        string='Type',
        required=True
    )

    categ_id = fields.Many2one(
        'product.category',
        'Category',
    )

    def action_icecat_api_call(self):
        self.ensure_one()

        for record in self:
            if not record.ean_upc or not record.language_id:
                raise UserError(_('EAN/UPC and Language are required'))

            url = "https://live.icecat.biz/api?shopname=openIcecat-live&lang=%s&content=&ean_upc=%s" % (record.language_id.iso_code, record.ean_upc)

            try:
                response = requests.get(url)
                response.raise_for_status()
                product_info = response.json()

                existing_product = self.env['product.template'].search(
                    [('ean_upc', '=', record.ean_upc)],
                    limit=1,
                )

                if len(existing_product) > 0:
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'type': 'warning',
                        'title': _("Warning"),
                        'message': _('Product is already registered in your database.')
                    })

                    return {
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'res_model': 'product.template',
                        'view_mode': 'form',
                        'res_id': existing_product.id,
                        'target': 'current',
                    }

                product_sheet = product_info['data']['GeneralInfo']
                product_image = product_info['data']['Image']
                product_features = product_info['data']['FeaturesGroups']

                product = self.env['product.template'].create({
                    'name': product_sheet['TitleInfo']['GeneratedIntTitle'],
                    'ean_upc': record.ean_upc,
                    'detailed_type': record.detailed_type,
                })

                if product_sheet['BrandPartCode']:
                    product.part_number_code = product_sheet['BrandPartCode']

                if record.categ_id:
                    product.categ_id = record.categ_id

                if product_sheet['SummaryDescription']['LongSummaryDescription']:
                    product.description_sale = product_sheet['SummaryDescription']['LongSummaryDescription']

                if product_sheet['BrandInfo']:
                    existing_manufacturer = self.env['product.manufacturer'].search(
                        [('name', '=', product_sheet['BrandInfo']['BrandName'])],
                        limit=1,
                    )

                    if len(existing_manufacturer) > 0:
                        if not product.product_manufacturer_id.image_1920:
                            product.product_manufacturer_id.image_1920 = base64.b64encode(requests.get(product_sheet['BrandInfo']['BrandLogo']).content)

                        product.product_manufacturer_id = existing_manufacturer[0].id
                    else:
                        manufacturer = self.env['product.manufacturer'].create({
                            'name': product_sheet['BrandInfo']['BrandName'],
                            'image_1920': base64.b64encode(requests.get(product_sheet['BrandInfo']['BrandLogo']).content)
                        })

                        product.product_manufacturer_id = manufacturer

                if product_image['HighPic']:
                    product.image_1920 = base64.b64encode(requests.get(product_image['HighPic']).content)


                for feature_group in product_features:
                    if feature_group['ID'] == 6881:
                        for feature in feature_group['Features']:
                            if feature['Feature']['ID'] == "94":
                                product.weight = float(feature['RawValue']) / 1000

                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'res_model': 'product.template',
                    'view_mode': 'form',
                    'res_id': product.id,
                    'target': 'current',
                }

            except requests.exceptions.HTTPError as http_err:
                # See 404, 500, etc. errors
                # print(f"HTTP error occurred: {http_err}")

                error_info = http_err.response.json()

                if error_info['Message']:
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'type': 'danger',
                        'title': _("Error"),
                        'message': _(error_info['Message'])
                    })

                pass
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
