/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {FormController} from '@web/views/form/form_controller';
import {useViewCompiler} from '@web/views/view_compiler';
import {FormCompiler} from '@web/views/form/form_compiler';
import {ButtonActions} from "./button_actions";


patch(FormController.prototype, {
    setup() {
        super.setup();

        const xmlDocHeaderButtons = this.archInfo.xmlDoc.querySelectorAll("header > button");

        if (xmlDocHeaderButtons.length > 0) {
            const header = document.createElement('header');

            xmlDocHeaderButtons.forEach(node => {
                header.appendChild(node.cloneNode(true));
            });

            const buttonActionsTemplates = useViewCompiler(
                this.props.Compiler || FormCompiler,
                {ButtonActions: header},
                {isSubView: true}
            );
            this.buttonActionsTemplate = buttonActionsTemplates.ButtonActions;
        }
    },
});

FormController.components.ButtonActions = ButtonActions;
