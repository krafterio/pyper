# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from bs4 import Stylesheet

from odoo import http
from odoo.addons.base.models.assetsbundle import ANY_UNIQUE, ScssStylesheetAsset
from odoo.http import request

ACCESSIBILITY_BUNDLE = 'pyper_accessibility.assets'

class DynamicCSSController(http.Controller):
    @http.route('/web/user_accessibility.css', type='http', auth='user')
    def user_style(self):
        variables = request.env.user.get_accessibility_scss_variables()

        for file_info in request.env['ir.qweb']._get_asset_content(ACCESSIBILITY_BUNDLE)[0]:
            if file_info['url'].rpartition('.')[2] != 'scss':
                continue

            filename = file_info['filename']
            bundle = request.env['ir.qweb']._get_asset_bundle(ACCESSIBILITY_BUNDLE, js=False)

            if not bundle.stylesheets:
                raise request.not_found()

            content_variables = self._generate_scss_variables_content(variables)

            if content_variables:
                bundle.stylesheets.insert(0, ScssStylesheetAsset(self, content_variables))

            attachment = bundle.css()

            if not attachment:
                raise request.not_found()

            stream = request.env['ir.binary']._get_stream_from(attachment, 'raw', filename)

            return stream.get_response(as_attachment=False, immutable=False, max_age=None)

        raise request.not_found()

    @staticmethod
    def _generate_scss_variables_content(variables):
        content = ''

        for variable, value in variables.items():
            content += '$' + variable + ': ' + value + ';\n'

        return content
