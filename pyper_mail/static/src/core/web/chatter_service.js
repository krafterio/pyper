/** @odoo-module **/

import { registry } from "@web/core/registry";
import {cookie} from '@web/core/browser/cookie';

export const ChatterService = {
    dependencies: [],

    start(env) {
        let isChatterVisible = cookie.get('chatter_visible') === 'true';

        return {
            hideChatter() {
                const chatter = document.querySelector('.oe_chatter');
                const formView = document.querySelector('.o_form_sheet_bg');

                chatter.classList.add("chatter-closed");
                chatter.classList.remove("chatter-slide-in");
                chatter.classList.add("chatter-slide-out");
                formView.classList.add("form-expand");
            },

            toggleChatter() {
                isChatterVisible = !isChatterVisible;
                cookie.set('chatter_visible', isChatterVisible);

                const chatter = document.querySelector('.oe_chatter');
                const formView = document.querySelector('.o_form_sheet_bg');

                if (chatter && formView) {
                    if (isChatterVisible) {
                        chatter.classList.remove("chatter-closed");
                        chatter.classList.remove("chatter-slide-out");
                        chatter.classList.add("chatter-slide-in");
                        formView.classList.remove("form-expand");
                    } else {
                        chatter.classList.remove("chatter-slide-in");
                        chatter.classList.add("chatter-slide-out");
                        formView.classList.add("form-expand");
                    }
                }
            },
        };
    },
};

registry.category("services").add("chatter", ChatterService);
