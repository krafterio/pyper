# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from odoo import _, http
from odoo.http import request
import logging
import base64
import uuid
import imghdr


_logger = logging.getLogger(__name__)
class PortalResPartnerRequest(http.Controller):

    @http.route('/my/requests', type='http', auth="user", website=True)
    def portal_my_request(self, **kw):
        user = request.env.user
        domain = [('author_parent_id', '=', user.partner_id.parent_id.id)]
        if not user.partner_id.parent_id:
            domain = [('author_id', '=', user.partner_id.id)]
            
        domain.append(('state', '!=', 'closed'))
        partner_requests = request.env['res.partner.request'].search(domain)
        waiting_requalification_requests = partner_requests.filtered(lambda r: r.state == 'awaiting_requalification')
        if request.env.user.has_group('pyper_partner_request.group_request_validator'):
            waiting_validation_requests = partner_requests.filtered(lambda r: r.state == 'waiting_for_validation')
            waiting_requalification_requests = waiting_requalification_requests | waiting_validation_requests

        return request.render('pyper_portal_partner_request.portal_my_requests_template', {
            'partner_requests': partner_requests,
            'waiting_requalification_requests': waiting_requalification_requests
        })
    
    @http.route('/my/requests/create', type='http', auth='user', website=True)
    def create_request_form(self, **kw):
        return request.render('pyper_portal_partner_request.portal_create_request_template', {})


    @http.route('/my/requests/create/submit', type='http', auth='user', methods=['POST'], website=True)
    def create_request(self, **post):
        partner_request_name = post.get('partner_request_name')
        partner_request_description = post.get('partner_request_description')
        partner_request_image = request.httprequest.files.get('partner_request_image')
        partner_request_attachment = post.get('partner_request_attachment')
        partner_request_category = post.get('partner_request_category')

        try:

            if partner_request_image:
                image_type = imghdr.what(partner_request_image)
                if image_type not in ['jpeg', 'png', 'gif']:
                    raise ValueError(_("Uploaded file is not a valid image"))
                img_base64 = base64.b64encode(partner_request_image.read())
                img_tag = '<br/> <img src="data:image/png;base64,%s" />' % img_base64.decode('utf-8')
                partner_request_description += img_tag

            partner_request = request.env['res.partner.request'].create({
                'name': partner_request_name,
                'description': partner_request_description,
                'priority': 'normal',
                'author_id': request.env.user.partner_id.id,
                'category': partner_request_category
            })
            if partner_request_attachment:
                self.create_attachment(partner_request, partner_request_attachment)
        except Exception as e:
            _logger.error("Failed to create request")
            print(f'Error: {e}')
            request.session['request_error'] = 'Failed to create request'
            return request.render('pyper_portal_partner_request.portal_create_request_template', {
                'error': True,
                'error_message': e
            })
        return request.redirect('/my/requests/%s' % partner_request.id)

    def create_attachment(self, partner_request, attachment):
        request.env['ir.attachment'].sudo().create({
            'name': attachment.filename,
            'datas': base64.b64encode(attachment.read()),
            'res_model': 'res.partner.request',
            'res_id': partner_request.id,
            'access_token': uuid.uuid4().hex
        })

    @http.route('/my/requests/<int:request_id>', type='http', auth='user', website=True)
    def portal_request_detail_view(self, request_id):
        partner_request = request.env['res.partner.request'].browse(request_id)
        attachments = request.env['ir.attachment'].sudo().search([('res_model', '=', 'res.partner.request'), ('res_id', '=', partner_request.id)])

        if partner_request.author_parent_id != request.env.user.partner_id.parent_id:
            return request.redirect('/my/requests')

        return request.render('pyper_portal_partner_request.portal_request_detail_view', {
            'partner_request': partner_request,
            'attachments': attachments
        })

    @http.route(['/portal/download/<int:attachment_id>'], type='http', auth="user", website=True)
    def download_attachment(self, attachment_id, **kwargs):
        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
        if not attachment.exists() or attachment.res_model != 'your.model':
            return request.not_found()

        file_content = base64.b64decode(attachment.datas)
        return request.make_response(
            file_content,
            headers=[
                ('Content-Type', attachment.mimetype or 'application/octet-stream'),
                ('Content-Disposition', 'attachment; filename=%s' % attachment.name),
            ]
        )


    @http.route('/my/requests/<int:request_id>/validate', type='http', auth='user', website=True)
    def validate_request(self, request_id):
        partner_request = request.env['res.partner.request'].sudo().browse(request_id)
        partner_request.action_validate()
        return request.redirect('/my/requests/%s' % partner_request.id)

    @http.route('/my/requests/<int:request_id>/ask_requalification', type='http', auth='user', website=True)
    def ask_for_requalification_request(self, request_id):
        partner_request = request.env['res.partner.request'].sudo().browse(request_id)
        partner_request.action_ask_requalification()
        return request.redirect('/my/requests/%s' % partner_request.id)
    
    @http.route('/my/requests/<int:request_id>/close', type='http', auth='user', website=True)
    def close_request(self, request_id):
        partner_request = request.env['res.partner.request'].sudo().browse(request_id)
        partner_request.action_close()
        return request.redirect('/my/requests/%s' % partner_request.id)

    @http.route('/my/requests/settings', type='http', auth='user', website=True)
    def portal_request_settings(self, **kw):
        users = request.env['res.users'].search([('partner_id.parent_id', '=', request.env.user.partner_id.parent_id.id)])
        return request.render('pyper_portal_partner_request.portal_partner_request_settings_template', {
            'partner': request.env.user.partner_id.parent_id,
            'users': users
        })

    @http.route('/my/requests/settings/update', type='http', auth='user', methods=['POST'], website=True)
    def update_settings(self, **post):
        user = request.env.user
        user.partner_id.parent_id.require_request_approval = post.get('require_request_approval')
        self.update_groups(post)
        return request.redirect('/my/requests/settings')

    def update_groups(self, post):
        for field in post:
            if field == 'require_request_approval':
                continue
            field_name = field.split('_')[0]
            field_user_id = field.split('_')[1]
            if field_name == 'user':
                user = request.env['res.users'].browse(int(field_user_id))
                self.set_groups(user, post)

    def set_groups(self, user, post):
        if post.get('validator_' + str(user.id)):
            user.sudo().write({'groups_id': [(4, request.env.ref('pyper_partner_request.group_request_validator').id)]})
        else:
            user.sudo().write({'groups_id': [(3, request.env.ref('pyper_partner_request.group_request_validator').id)]})
        if post.get('creator_' + str(user.id)):
            user.sudo().write({'groups_id': [(4, request.env.ref('pyper_partner_request.group_request_creator').id)]})
        else:
            user.sudo().write({'groups_id': [(3, request.env.ref('pyper_partner_request.group_request_creator').id)]})

    @http.route('/my/requests/filter', type='http', auth='user', website=True)
    def filter_request(self, **kw):
        user = request.env.user
        state = kw.get('state')
        domain = [('author_parent_id', '=', user.partner_id.parent_id.id)]
        if state != 'all':
            domain.append(('state', '=', state))
        partner_requests = request.env['res.partner.request'].sudo().search(domain)
        return request.render('pyper_portal_partner_request.portal_my_requests_template', {
            'partner_requests': partner_requests
        })