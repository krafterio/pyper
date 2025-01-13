/* @odoo-module */

import {patch} from '@web/core/utils/patch';
import {Drawer} from '@pyper_drawer/webclient/drawer/drawer';
import {GlobalSearchInput} from '@pyper_global_search/webclient/global_search/global_search_input';

patch(Drawer.prototype, {
    setup() {
        this.constructor.components.GlobalSearchInput = GlobalSearchInput;
        super.setup();
    },
});
