/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";
import { useState, onMounted } from "@odoo/owl";
import {cookie} from '@web/core/browser/cookie';

patch(FormController.prototype, {
    setup() {
        super.setup();
        this.chatterService = useService("chatter");

        this.state = useState({
            hasChatter: false,
        });

        onMounted(() => {
            let chatter = document.querySelector('.oe_chatter');
            this.state.hasChatter = chatter && chatter.classList.contains('o-aside');
            if (cookie.get('chatter_visible') === 'false' && this.state.hasChatter) {
                this.chatterService.hideChatter();
            }
        });
    },

    toggleChatterFromForm() {
        this.chatterService.toggleChatter();
    },
});
