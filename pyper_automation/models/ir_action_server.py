# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class IrActionServer(models.Model):
    _inherit = 'ir.actions.server'

    sms_number_field = fields.Many2one(
        'ir.model.fields',
        'Phone number field',
        help='Allow to force use a custom phone number field of selected model to send a SMS message',
    )

    sms_number_field_domain = fields.Binary(
        compute='_compute_sms_number_field_domain',
    )

    sms_country_field = fields.Many2one(
        'ir.model.fields',
        'Phone country field',
        help='Allow to force use a custom phone country field of selected model to send a SMS message',
    )

    sms_country_field_domain = fields.Binary(
        compute='_compute_sms_country_field_domain',
    )

    @api.depends('model_id')
    def _compute_sms_number_field_domain(self):
        for record in self:
            record.sms_number_field_domain = [
                ('model_id', '=', record.model_id.id),
                ('ttype', 'in', ['char'])
            ]

    @api.depends('model_id')
    def _compute_sms_country_field_domain(self):
        for record in self:
            record.sms_country_field_domain = [
                ('model_id', '=', record.model_id.id),
                ('ttype', 'in', ['many2one'])
            ]

    @api.onchange('model_id')
    def _onchange_model_id(self):
        for record in self:
            record.sms_number_field = False

    @api.onchange('model_id', 'sms_number_field')
    def _onchange_model_id_sms_number_field(self):
        for record in self:
            record.sms_country_field = False

    def _run_action_sms_multi(self, eval_context=None):
        # Override action sms to add custom number field of base automation in composer
        if self.sms_number_field:
            # TDE CLEANME: when going to new api with server action, remove action
            if not self.sms_template_id or self._is_recompute():
                return False

            records = eval_context.get('records') or eval_context.get('record')
            if not records:
                return False

            composer = self.env['sms.composer'].with_context(
                default_res_model=records._name,
                default_res_ids=records.ids,
                default_composition_mode='comment' if self.sms_method == 'comment' else 'mass',
                default_template_id=self.sms_template_id.id,
                default_mass_keep_log=self.sms_method == 'note',
                default_number_field_name=self.sms_number_field.name,
                sms_country_field_name=self.sms_country_field.name,
            ).create({})
            composer.action_send_sms()
            return False

        return super()._run_action_sms_multi(eval_context)
