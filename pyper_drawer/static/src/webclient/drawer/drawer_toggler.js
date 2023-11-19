/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';


export class DrawerToggler extends Component {
    static template = 'pyper_drawer.DrawerToggler';

    static description = 'Toggler of Drawer';

    static props = {
        autoHide: {
            type: Boolean,
            optional: true,
        },
        useCaretIcon: {
            type: Boolean,
            optional: true,
        },
    }

    static defaultProps = {
        autoHide: false,
        useCaretIcon: false,
    }

    setup() {
        this.drawerService = useState(useService('drawer'));
    }

    get classes() {
        return {
            'o-dropdown': true,
            'dropdown': true,
            'o_drawer_toggler': true,
            'o-dropdown--no-caret': true,
            'o_drawer--locked': this.drawerService.isLocked,
            'o_drawer--mini': this.drawerService.isMinified,
            'o_drawer--fixed-top': this.drawerService.isFixedTop,
        };
    }

    get displayMenuIcon() {
        return !this.props.useCaretIcon || (this.props.useCaretIcon && !this.drawerService.isMinified);
    }

    get displayCaretIcon() {
        return this.props.useCaretIcon && this.drawerService.isMinified;
    }

    get display() {
        return !(this.props.autoHide && this.drawerService.isLocked) && !this.drawerService.disabledOnSmallScreen;
    }

    onClick() {
        this.drawerService.toggle();
    }
}
