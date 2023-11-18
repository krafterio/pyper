/** @odoo-module **/

import {
    Component,
    useState,
    onWillUnmount,
} from '@odoo/owl';
import {registry} from '@web/core/registry';

const drawerRegistry = registry.category('drawer');

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
        this.state = useState({
            drawerLocked: drawerRegistry.get('locked', false),
            drawerMini: drawerRegistry.get('mini', false),
            disabledOnSmallScreen: drawerRegistry.get('disabledOnSmallScreen', false),
        });

        const drawerListener = () => {
            this.state.drawerLocked = drawerRegistry.get('locked', false);
            this.state.drawerMini = drawerRegistry.get('mini', false);
            this.state.disabledOnSmallScreen = drawerRegistry.get('disabledOnSmallScreen', false);
        };

        drawerRegistry.addEventListener('UPDATE', drawerListener);

        onWillUnmount(() => {
            drawerRegistry.removeEventListener('UPDATE', drawerListener);
        });
    }

    get classes() {
        return {
            'o-dropdown': true,
            'dropdown': true,
            'o_drawer_toggler': true,
            'o-dropdown--no-caret': true,
            'o_drawer--locked': this.state.drawerLocked,
            'o_drawer--mini': this.state.drawerMini,
        };
    }

    get displayMenuIcon() {
        return !this.props.useCaretIcon || (this.props.useCaretIcon && !this.state.drawerMini);
    }

    get displayCaretIcon() {
        return this.props.useCaretIcon && this.state.drawerMini;
    }

    get display() {
        return !(this.props.autoHide && this.state.drawerLocked) && !this.state.disabledOnSmallScreen;
    }

    onClick() {
        this.env.bus.trigger('DRAWER:TOGGLE');
    }
}
