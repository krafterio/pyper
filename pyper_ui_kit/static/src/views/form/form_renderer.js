/** @odoo-module **/

import {FormRenderer} from '@web/views/form/form_renderer';
import {ButtonActions} from './button_actions';
import {patch} from '@web/core/utils/patch';

patch(FormRenderer.prototype, {
    setup() {
        this.constructor.components.ButtonActions = ButtonActions;
        this.constructor.components.SheetButtonBox = FormRenderer.components.ButtonBox;
        super.setup();
    },
});
