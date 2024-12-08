/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {createElement} from '@web/core/utils/xml';
import {FormController} from '@web/views/form/form_controller';
import {FormCompiler} from '@web/views/form/form_compiler';
import {useViewCompiler} from '@web/views/view_compiler';
import {ButtonActions} from './button_actions';


patch(FormController.prototype, {
    setup() {
        super.setup();

        this._moveHeaderButtonsInControlPanel();
        this._moveStatusbarInControlPanel();
        this._moveButtonBoxInSheet();
    },

    /**
     * Move header buttons in button actions component for control panel.
     *
     * @private
     */
    _moveHeaderButtonsInControlPanel() {
        const xmlDocHeaderButtons = this.archInfo.xmlDoc.querySelectorAll('header > button');

        if (xmlDocHeaderButtons.length > 0) {
            const buttonActions = createElement('div', {'name': 'o_button_actions'});

            xmlDocHeaderButtons.forEach(node => {
                buttonActions.appendChild(node);
            });

            const buttonActionsTemplates = useViewCompiler(
                this.props.Compiler || FormCompiler,
                {ButtonActions: buttonActions},
                {isSubView: true},
            );
            this.buttonActionsTemplate = buttonActionsTemplates.ButtonActions;
        }
    },

    /**
     * Move statusbar ('header' element in arch) in control panel.
     *
     * @private
     */
    _moveStatusbarInControlPanel() {
        const xmlHeader = this.archInfo.xmlDoc.querySelector('header');

        if (xmlHeader) {
            const statusbar = createElement('div', {'class': 'o_form_statusbar'});

            for (const node of xmlHeader.children) {
                statusbar.appendChild(node.cloneNode(true));
            }

            const statusbarTemplates = useViewCompiler(
                this.props.Compiler || FormCompiler,
                {Statusbar: statusbar},
                {isSubView: true},
            );
            this.statusbarTemplate = statusbarTemplates.Statusbar;

            xmlHeader.remove();
        }
    },

    /**
     * Move button box in sheet.
     * @private
     */
    _moveButtonBoxInSheet() {
        const xmlSheet = this.archInfo.xmlDoc.querySelector('sheet');
        const xmlButtonBox = this.archInfo.xmlDoc.querySelector('div[name="button_box"]');

        if (xmlSheet && xmlButtonBox) {
            const xmlSheetButtonBox = xmlButtonBox.cloneNode(true);
            xmlSheetButtonBox.classList.remove('oe_button_box');
            xmlSheetButtonBox.setAttribute('name', 'sheet_button_box');
            xmlSheet.prepend(xmlSheetButtonBox);

            xmlButtonBox.remove();
            delete this.buttonBoxTemplate;
        }
    },
});

FormController.components.ButtonActions = ButtonActions;
