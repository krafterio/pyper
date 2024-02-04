/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ThreadService} from '@mail/core/common/thread_service';

patch(ThreadService.prototype,  {
    async insertSuggestedRecipients(thread, dataList) {
        thread.suggestedRecipients = [];
    },
});
