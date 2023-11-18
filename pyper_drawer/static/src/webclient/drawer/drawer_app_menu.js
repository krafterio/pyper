/** @odoo-module **/

import {
    Component,
    useState,
    onWillUnmount,
} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {listenSizeChange, SIZES, utils as uiUtils} from '@web/core/ui/ui_service';

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
            size: uiUtils.getSize(),
        });

        const drawerListener = () => {
            this.state.drawerLocked = drawerRegistry.get('locked', false);
            this.state.drawerMini = drawerRegistry.get('mini', false);
        };

        drawerRegistry.addEventListener('UPDATE', drawerListener);

        onWillUnmount(() => {
            drawerRegistry.removeEventListener('UPDATE', drawerListener);
        });

        listenSizeChange(() => {
            this.state.size = uiUtils.getSize();
        });
    }

    get isLocked() {
        return this.state.drawerLocked;
    }

    get isMinified() {
        return this.state.drawerMini;
    }

    get displayMinified() {
        return this.isMinified || this.isSmallScreen || this.props.minified;
    }

    get isSmallScreen() {
        return uiUtils.getSize() <= SIZES.LG;
    }
}
