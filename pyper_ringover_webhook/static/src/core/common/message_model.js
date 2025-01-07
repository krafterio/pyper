/* @odoo-module */

import {patch} from '@web/core/utils/patch';
import {Message} from '@mail/core/common/message_model';

patch(Message.prototype, {
    get isEmpty() {
        if (['phone_outbound', 'phone_inbound'].includes(this.type)) {
            return false;
        }

        return super.isEmpty;
    },
});
