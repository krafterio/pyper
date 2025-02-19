/* @odoo-module */

import { Chatter } from "@mail/core/web/chatter";
import { patch } from '@web/core/utils/patch';
import { onMounted } from "@odoo/owl";

patch(Chatter.prototype, {
    setup() {
        super.setup();
        onMounted(() => {
            this.toggleComposer("message");
        });

    },
});