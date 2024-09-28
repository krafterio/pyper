/** @odoo-module **/

import {useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {patch} from '@web/core/utils/patch';
import {NavBar} from '@web/webclient/navbar/navbar';

patch(NavBar.prototype, {
    setup() {
        super.setup();
        this.menuStateService = useState(useService('menu_state'));
    },

    get systemTrayItems() {
        const menu = this.menuService.getMenuAsTree('root');
        const items = [];

        (menu.childrenTree || []).forEach((menu) => {
            if ('system_tray' === menu.category) {
                items.push({
                    ...menu,
                    isActive: this.menuStateService.activeIds.includes(menu.id),
                });
            }
        });

        return items;
    },
});
