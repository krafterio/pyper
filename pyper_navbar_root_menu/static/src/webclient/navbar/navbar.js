/** @odoo-module **/

import {NavBar} from '@web/webclient/navbar/navbar';
import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';

patch(NavBar.prototype, {
    get rootAppSections() {
        const menu = this.menuService.getMenuAsTree('root');

        return menu.childrenTree || [];
    },

    get rootCategoryAppSections() {
        const categories = {};

        this.rootAppSections.forEach((menu) => {
            if (undefined === categories[menu.category]) {
                categories[menu.category] = {
                    display_name: menu.category_display_name || _t('Other'),
                    value: menu.category || 'other',
                    menus: [],
                }
            }

            categories[menu.category]['menus'].push(menu);
        });

        return categories;
    },

    get rootMainCategoryAppSections() {
        const categories = {...this.rootCategoryAppSections};
        delete categories['system_tray'];

        return categories;
    },

    get rootMainAppSections() {
        const menus = [];

        Object.values(this.rootMainCategoryAppSections).forEach((category) => {
            category.menus.forEach((menu) => {
                const newMenu = {...menu};
                newMenu.childrenTree = [];
                menus.push(newMenu);
            });
        });

        return menus;
    },

    get systemTraySections() {
        if (this.rootCategoryAppSections['system_tray']
            && this.rootCategoryAppSections['system_tray']['menus'].length > 0
        ) {
            return this.rootCategoryAppSections['system_tray']['menus'];
        }

        return [];
    },

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
