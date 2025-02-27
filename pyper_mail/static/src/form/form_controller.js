/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";
import {
    useState,
    onMounted,
    useExternalListener,
} from "@odoo/owl";
import {cookie} from '@web/core/browser/cookie';
import {debounce} from '@web/core/utils/timing';

patch(FormController.prototype, {
    setup() {
        super.setup();
        this.chatterService = useService("chatter");

        this.state = useState({
            hasChatter: false,
            chatteOpen: true,
        });

        const updateToggleButtonVisibility = () => {
            let chatter = document.querySelector('.o-mail-ChatterContainer');
            this.state.hasChatter = chatter && chatter.classList.contains('o-aside');
        }

        onMounted(() => {
            let chatter = document.querySelector('.o-mail-ChatterContainer');
            this.state.hasChatter = chatter && chatter.classList.contains('o-aside');
            if (cookie.get('chatter_visible') === 'false')
                this.state.chatterOpen = false;

            if (cookie.get('chatter_visible') === 'false' && this.state.hasChatter) {
                this.chatterService.hideChatter();
            }
        });

        useExternalListener(window, 'resize', updateToggleButtonVisibility);
    },

    toggleChatterFromForm() {
        this.chatterService.toggleChatter();
        this.state.chatterOpen = cookie.get('chatter_visible') === 'true'
    },
});
