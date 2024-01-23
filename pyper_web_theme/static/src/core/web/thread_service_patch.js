/** @odoo-module */

import { patch } from '@web/core/utils/patch';
import { ThreadService, threadService } from "@mail/core/common/thread_service";
import { parseEmail } from "@mail/js/utils";
let nextId = 1;

patch(ThreadService.prototype,  {
    async insertSuggestedRecipients(thread, dataList) {
        const recipients = [];
        thread.suggestedRecipients = recipients;
    },
})