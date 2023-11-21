/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';


export class OverlayMenuToggler extends Component {
    static template = 'pyper_overlay_menu.OverlayMenuToggler';

    static props = {};

    setup() {
        this.overlayMenuService = useState(useService('overlay_menu'));
    }

    get classes() {
        return {
            'dropdown': true,
            'o-dropdown': true,
            'o-dropdown--no-caret': true,
            'o_overlay_menu_toggler': true,
        };
    }

    onClick() {
        this.overlayMenuService.toggle();
    }
}
