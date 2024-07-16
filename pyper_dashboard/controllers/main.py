# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from lxml import etree as ElementTree

from odoo.http import Controller, route, request


class Dashboard(Controller):
    @route('/dashboard/add_to_dashboard', type='json', auth='user')
    def add_to_dashboard(self, action_id, context_to_save, domain, view_mode, board_id=None, name=''):
        if board_id:
            return _add_to_board_dashboard(action_id, context_to_save, domain, view_mode, board_id, name)

        return _add_to_my_dashboard(action_id, context_to_save, domain, view_mode, name)


def _add_to_board_dashboard(action_id, context_to_save, domain, view_mode, board_id, name=''):
    board = request.env['dashboard.dashboard'].browse(board_id)

    view_id = request.env.ref('pyper_dashboard.view_dashboard_dashboard', False).sudo()

    if view_id:
        board_arch = ElementTree.fromstring(board.arch or view_id.arch)
        arch = _update_arch(board_arch, action_id, context_to_save, domain, view_mode, name)

        if arch:
            board.write({
                'arch': arch,
            })

            return True

    return False


def _add_to_my_dashboard(action_id, context_to_save, domain, view_mode, name=''):
    action = request.env.ref('pyper_dashboard.action_my_dashboard_open', False).sudo()

    if action and action['res_model'] == 'dashboard.board' and action['views'][0][1] == 'form' and action_id:
        view_id = action['views'][0][0]
        dashboard_view = request.env['dashboard.board'].get_view(view_id, 'form')

        if dashboard_view and 'arch' in dashboard_view:
            board_arch = ElementTree.fromstring(dashboard_view['arch'])
            arch = _update_arch(board_arch, action_id, context_to_save, domain, view_mode, name)

            if arch:
                custom_view = request.env['ir.ui.view.custom'].sudo().search([
                    ('user_id', '=', request.session.uid),
                    ('ref_id', '=', view_id),
                ], limit=1)

                if custom_view:
                    custom_view.write({
                        'arch': arch,
                    })
                else:
                    custom_view.create({
                        'user_id': request.session.uid,
                        'ref_id': view_id,
                        'arch': arch,
                    })

                return True

    return False


def _update_arch(board_arch, action_id, context_to_save, domain, view_mode, name=''):
    columns = board_arch.xpath('//dashboard/section/column')
    column = columns[len(columns) - 1] if len(columns) > 1 else None

    if column is None:
        sections = board_arch.xpath('//dashboard/section')
        section = sections[len(sections) - 1] if len(sections) > 1 else None

        if section is None:
            section = ElementTree.Element('section')
            board_arch.insert(0, section)

        if section is not None:
            column = ElementTree.Element('column')
            section.insert(0, column)

    if column is not None:
        if 'allowed_company_ids' in context_to_save:
            context_to_save.pop('allowed_company_ids')

        new_action = ElementTree.Element('action', {
            'name': str(action_id),
            'string': name,
            'view_mode': view_mode,
            'context': str(context_to_save),
            'domain': str(domain)
        })
        column.insert(0, new_action)

        return ElementTree.tostring(board_arch, encoding='unicode')
