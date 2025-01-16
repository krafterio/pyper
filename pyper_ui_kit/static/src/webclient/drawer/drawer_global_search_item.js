/* @odoo-module */

import {patch} from '@web/core/utils/patch';
import {DrawerGlobalSearchItem} from '@pyper_drawer_global_search/webclient/drawer/drawer_global_search_item';

patch(DrawerGlobalSearchItem.prototype, {
    get fontIcon() {
        return 'ph ph-magnifying-glass';
    },
});
