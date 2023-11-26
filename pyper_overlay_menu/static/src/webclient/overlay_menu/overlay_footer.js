/** @odoo-module **/

import {Component} from '@odoo/owl';
import {isMacOS} from '@web/core/browser/feature_detection';


export class OverlayFooter extends Component {
    static template = 'pyper_overlay_menu.OverlayMenu.CommandPalette.Footer';

    static props = {
        switchNamespace: {
            type: Function,
            optional: true,
        },
    }

    setup() {
        this.controlKey = isMacOS() ? 'COMMAND' : 'CONTROL';
    }
}
