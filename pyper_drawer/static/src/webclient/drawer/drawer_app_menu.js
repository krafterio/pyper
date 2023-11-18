/** @odoo-module **/

import {
    Component,
    useState,
    onWillUnmount,
} from '@odoo/owl';
import {registry} from '@web/core/registry';

const drawerRegistry = registry.category('drawer');

export class DrawerAppMenu extends Component {
    static description = 'App menu of Drawer';

    static template = 'pyper_drawer.DrawerAppMenu';

    static props = {
        minified: {
            type: Boolean,
            optional: true,
        },
    }

    static defaultProps = {
        minified: false,
    }

    setup() {
        this.state = useState({
            drawerLocked: drawerRegistry.get('locked', false),
            drawerMini: drawerRegistry.get('mini', false),
            drawerIsSmallScreen: drawerRegistry.get('isSmallScreen', false),
        });

        const drawerListener = () => {
            this.state.drawerLocked = drawerRegistry.get('locked', false);
            this.state.drawerMini = drawerRegistry.get('mini', false);
            this.state.drawerIsSmallScreen = drawerRegistry.get('isSmallScreen', false);
        };

        drawerRegistry.addEventListener('UPDATE', drawerListener);

        onWillUnmount(() => {
            drawerRegistry.removeEventListener('UPDATE', drawerListener);
        });
    }

    get displayMinified() {
        return this.state.drawerMini || this.state.drawerIsSmallScreen || this.props.minified;
    }

    get displayLocked() {
        return !this.displayMinified && this.state.drawerLocked;
    }
}
