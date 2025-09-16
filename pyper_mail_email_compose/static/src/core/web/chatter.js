/** @odoo-module */

import {Chatter} from '@mail/chatter/web_portal/chatter';
import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {rpc} from '@web/core/network/rpc';

patch(Chatter.prototype, {
    get thread() {
        return this.threadService.store.Thread.get({
            model: this.props.threadModel,
            id: this.props.threadId,
        });
    },

    async onClickSendEmail() {
        // Auto-create partners of checked suggested partners
        const newPartners = this.thread.suggestedRecipients.filter(
            (recipient) => recipient.checked && !recipient.persona
        );

        if (newPartners.length !== 0) {
            const recipientEmails = [];
            const recipientAdditionalValues = {};

            newPartners.forEach((recipient) => {
                recipientEmails.push(recipient.email);
                recipientAdditionalValues[recipient.email] =
                    recipient.defaultCreateValues || {};
            });

            const partners = await rpc('/mail/partner/from_email', {
                emails: recipientEmails,
                additional_values: recipientAdditionalValues,
            });

            for (const index in partners) {
                const partnerData = partners[index];
                const persona = this.store.Persona.insert({...partnerData, type: 'partner'});
                const email = recipientEmails[index];
                const recipient = this.thread.suggestedRecipients.find(
                    (recipient) => recipient.email === email
                );
                Object.assign(recipient, {persona});
            }
        }

        const partnerIds = [
            ...this.thread.suggestedRecipients
                .filter((recipient) => recipient.checked)
                .map((recipient) => recipient.persona.id),
            ...this.thread.followers
                .filter((recipient) => !!recipient.partner_id)
                .map((recipient) => recipient.partner_id),
        ];

        const context = {
            default_attachment_ids: [],
            default_body: undefined,
            default_model: this.thread.model,
            default_partner_ids: partnerIds,
            default_res_ids: [this.thread.id],
            default_subtype_xmlid: 'mail.mt_activities',
            mail_post_autofollow: this.thread.hasWriteAccess,
            mail_email_compose: true,
        };

        const action = {
            name: _t('Compose Email'),
            type: 'ir.actions.act_window',
            res_model: 'mail.compose.message',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: context,
        };

        const options = {
            onClose: () => {
                if (this.thread) {
                    this.threadService.fetchNewMessages(this.thread);
                }
            },
        };

        await this.env.services.action.doAction(action, options);
    },
});
