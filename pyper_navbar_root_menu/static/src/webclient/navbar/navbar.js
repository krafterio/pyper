/** @odoo-module **/

import {NavBar} from '@web/webclient/navbar/navbar';
import {useService} from '@web/core/utils/hooks';
import {patch} from '@web/core/utils/patch';

patch(NavBar.prototype, {
    onNavBarDropdownItemSelection(menu) {
        super.onNavBarDropdownItemSelection(menu);

        // Force app changed to refresh the selection of menu
        if (menu) {
            this.env.bus.trigger("MENUS:APP-CHANGED");
        }
    },

    sectionIsSelected(menu) {
        if (this.currentApp && menu) {
            menu = typeof menu === 'number' ? this.menuService.getMenu(menu) : menu;

            const getAllChildren = function(menu) {
                const ids = [];

                ids.push(...(menu.children || []));

                (menu.childrenTree || []).forEach((childMenu) => {
                    ids.push(...getAllChildren(childMenu));
                });

                return ids;
            }

            // Check if selected menu is in sub menu or in children
            if (menu.id === this.menuService.currentMenuId
                || getAllChildren(menu).includes(this.menuService.currentMenuId)
            ) {
                return true;
            }

            // Check if selected menu is currentApp and if it is the case, check if the first sub menu is the same menu
            const currentApp = this.menuService.getCurrentApp();

            return currentApp.id === this.menuService.currentMenuId && currentApp?.childrenTree[0]?.id === menu.id;
        }

        return false;
    },
});
