from odoo import api, fields, models


class UnsubscribePartnersWizard(models.TransientModel):
    _name = 'wizard.unsubscribe.partners'
    _description = 'Unsubscribe Partners Confirmation'

    model_ids = fields.Many2many(
        'ir.model',
        string='Models',
        help='Select the models for which you want to unsubscribe partners.',
        domain=lambda self: [(
            'model', 'in', self.env['ir.model'].search([
                '|', ('model', '=', 'res.partner'), '&',
                # Filter models that inherits 'mail.thread'
                (
                    'model',
                    'in',
                    list(self.env['mail.thread.main.attachment']._inherit_children)
                    + list(self.env['mail.thread']._inherit_children)
                ),
                # Filter models that has a storabe 'partner_id' field
                ('model', 'in', self.env['ir.model.fields'].search([
                    ('name', '=', 'partner_id'),
                    ('store', '=', True)
                ]).mapped('model')),
            ]).mapped('model')
        )]
    )

    follower_ids = fields.Many2many('mail.followers', compute='_compute_follower_ids', readonly=False)

    @api.depends('model_ids')
    def _compute_follower_ids(self):
        if not self.model_ids:
            self.follower_ids = False
            return

        queries = self.model_ids.mapped(lambda m: f'''
                SELECT f.id
                FROM mail_followers f
                JOIN {self.env[m.model]._table} res ON res.id = f.res_id
                WHERE f.res_model = '{m.model}'
                AND f.partner_id = res.{'id' if m.model == 'res.partner' else 'partner_id'}
            ''')
        query = '''
        UNION
        '''.join(queries)
        self.env.cr.execute(query)
        self.follower_ids = [row[0] for row in self.env.cr.fetchall()]

    def action_confirm(self):
        self.follower_ids.unlink()
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
