/* @odoo-module */

import { ThreadService, threadService } from "@mail/core/common/thread_service";

import { patch } from "@web/core/utils/patch";

patch(ThreadService.prototype, {
    /**
     * @param {import("@web/env").OdooEnv} env
     * @param {Partial<import("services").Services>} services
     */
    setup(env, services) {
        super.setup(env, services);
        this.recipient_default_checked_promise = this.orm.call(
            'mail.thread',
            'get_msg_post_recipients_default_checked',
            [''],
        ).catch(err => {
            console.error('An error occured: ', err);
            return false
        });
    },

    /**
     * @param {import("models").Thread} thread
     * @param {import("@mail/core/web/suggested_recipient").SuggestedRecipient[]} dataList
     */
    async insertSuggestedRecipients(thread, dataList) {
        super.insertSuggestedRecipients(thread,dataList);
        const recipient_default_checked = await this.recipient_default_checked_promise;
        thread.suggestedRecipients.forEach(recipient => recipient.checked = recipient_default_checked);
    },
});

patch(threadService, {
    dependencies: [...threadService.dependencies, "action", "mail.activity", "mail.chat_window"],
});
