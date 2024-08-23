# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models, tools
from odoo.exceptions import UserError


class PiloterrWebsiteCrawler(models.Model):
    _name = 'piloterr.website.crawler'
    _inherit = ['piloterr.mixin']
    _description = 'Piloterr Website Crawler'

    def fetch_html(
        self,
        delay: bool,
        header: dict = None,
        param_url: list = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: str = None
    ):

        model = self.env[model_name].browse(obj_id)

        if not model.website:
            raise UserError(_('You have to give a website to complete operation.'))

        param_url = {
            'query': model.website,
        }

        self.call_piloterr_request(
            request_type='get',
            delay=delay,
            url=['website', 'crawler'],
            header=header,
            param_url=param_url,
            callback=callback,
            model_name=model_name,
            obj_id=obj_id,
            field_name=field_name
        )

    def get_html(
        self,
        response: str,
        model_name: str,
        obj_id: int,
        field_name: str
    ):
        """
        This function assigns the HTML content from the request response
        to the specified object and uses it after to modify or display it

        :param response: The HTML content returned from the request
        :param model_name: The name of the model where is field_name
        :param obj_id: The object identifier where field_name needs to be updated with the HTML content.
        :param field_name: Not used but necessary when call get_html in the request
        """
        obj = self.env[model_name].browse(obj_id)

        self.env['crawler.result'].create({
            'html_content': response,
            'related_model': obj._name,
            'related_id': obj.id,
        })

    def get_clean_html(
        self,
        response: str,
        model_name: str,
        obj_id: int,
        field_name: str,
        silent: bool = True,
        sanitize_tags: bool = True,
        sanitize_attributes: bool = True,
        sanitize_style: bool = True,
        sanitize_form: bool = True,
        strip_style: bool = True,
        strip_classes: bool = True
    ):
        """
        This function sanitizes the HTML content from the request response
        and assigns the cleaned HTML to the specified object and uses it
        after to modify or display it

        :param response: The HTML content returned from the request
        :param model_name: The name of the model where is field_name
        :param obj_id: The object identifier where field_name needs to be updated with the HTML content.
        :param field_name: The name of the field in the object where the HTML content should be stored.
        :param silent: If True, suppresses errors during sanitization. Default is True.
        :param sanitize_tags: If True, sanitizes HTML tags. Default is True.
        :param sanitize_attributes: If True, sanitizes HTML attributes. Default is False.
        :param sanitize_style: If True, sanitizes inline CSS styles. Default is False.
        :param sanitize_form: If True, removes HTML form tags. Default is True.
        :param strip_style: If True, strips all style tags and attributes. Default is False.
        :param strip_classes: If True, removes CSS class attributes. Default is False.
        """
        cleaned_html = tools.html_sanitize(
            src=response,
            silent=silent,
            sanitize_tags=sanitize_tags,
            sanitize_attributes=sanitize_attributes,
            sanitize_style=sanitize_style,
            sanitize_form=sanitize_form,
            strip_style=strip_style,
            strip_classes=strip_classes
        )
        obj = self.env[model_name].browse(obj_id)

        self.env['crawler.result'].create({
            'html_content': cleaned_html,
            'related_model': obj._name,
            'related_id': obj.id,
        })
