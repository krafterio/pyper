/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { StatusBarField, statusBarField } from "@web/views/fields/statusbar/statusbar_field";
import { patch } from '@web/core/utils/patch';

patch(StatusBarField.prototype, {

    props : {
        ...StatusBarField.props,
        effect: { type: Object, optional: true },
    },

    setup() {
        super.setup();
        this.effect = useService("effect");
    },

    async selectItem(item) {
        console.log()
        await super.selectItem(item);
        if (this.props.effect) {
            this.handleClick(item.value);
        }
    },

    async handleClick(state) {
        debugger;
        const effect = this.props.effect;
    
        if (effect[state]) {
            const imgUrl = effect[state].url;
            const message = effect[state].message;
            const fadeout = effect[state].fadeout;

            const messageDynamic = this.props.record.data.messageEffect;
            const urlDynamic = this.props.record.data.urlEffect;

                await this.effect.add(

                    {
                    message: message || messageDynamic,
                    type: "rainbow_man",
                    fadeout: fadeout,
                    img_url: imgUrl || urlDynamic,
                });
    
            } else {
                console.warn(`Message template or message is missing for the state: ${state}`);
            }
    },
});

const extendedStatusBarField = () => ({
    extractProps({ options }) {
        const props = super.extractProps(...arguments);
        props.effect = options.effect;
        return props;
    },
    supportedOptions: [{
        label: ("Effect"),
        name: "effect",
        type: "Object",
        default: false,
    }],
});

patch(statusBarField, extendedStatusBarField());
