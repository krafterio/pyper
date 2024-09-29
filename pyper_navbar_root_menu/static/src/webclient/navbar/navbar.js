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
});
