/* @odoo-module */

import {patch} from '@web/core/utils/patch';
import {Message} from '@mail/core/common/message';

patch(Message.prototype, {
    get isPhoneLog() {
        return ['phone_outbound', 'phone_inbound'].includes(this.message?.type);
    },
});
