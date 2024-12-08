/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ThreadService} from '@mail/core/common/thread_service';

patch(ThreadService.prototype, {
    chatterWithAuditLog: false,

    /**
     * @param {import('@web/env').OdooEnv} env
     * @param {Partial<import('services').Services>} services
     */
    setup(env, services) {
        super.setup(env, services);
        this.chatterWithAuditLog = false;
    },

    getFetchParams(thread) {
        const res = super.getFetchParams(thread);

        if (thread.type === 'chatter') {
            res['audit_log'] = this.chatterWithAuditLog;
        }

        return res;
    },
});
