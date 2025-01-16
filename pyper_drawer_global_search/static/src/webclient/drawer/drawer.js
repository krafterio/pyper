/* @odoo-module */

import {patch} from '@web/core/utils/patch';
import {Drawer} from '@pyper_drawer/webclient/drawer/drawer';
import {DrawerGlobalSearchItem} from './drawer_global_search_item';

patch(Drawer.prototype, {
    setup() {
        this.constructor.components.DrawerGlobalSearchItem = DrawerGlobalSearchItem;
        super.setup();
    },
});
