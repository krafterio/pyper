/* @odoo-module */

import {ThreadService} from '@mail/core/common/thread_service';
import {patch} from '@web/core/utils/patch';


patch(ThreadService.prototype, {
    /**
     * @param {import("@web/env").OdooEnv} env
     * @param {Partial<import("services").Services>} services
     */
    setup(env, services) {
        super.setup(env, services);

        this.defaultSuggestedRecipientChecked = false;

        this.orm.call('mail.thread', 'get_msg_post_recipients_default_checked', [''])
            .then(defaultValue => {
                this.defaultSuggestedRecipientChecked = defaultValue;
            })
            .catch(err => {
                console.error('An error occured: ', err);
                return false;
            });
    },
});
