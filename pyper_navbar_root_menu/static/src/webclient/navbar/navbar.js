/** @odoo-module **/

import {NavBar} from '@web/webclient/navbar/navbar';
import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';

patch(NavBar.prototype, {
    get rootMainCategoryAppSections() {
        const rootMenu = this.menuService.getMenuAsTree('root');
        const menus = rootMenu.childrenTree || [];

        const categories = {};

        menus.forEach((menu) => {
            if (menu.position) {
                return;
            }

            const menuCatId = menu.category ? menu.category[0] : undefined;
            const menuCatName = menu.category ? menu.category[1] : undefined;
            const menuCatSeq = menu.categorySequence ? menu.categorySequence : undefined;

            if (undefined === categories[menuCatId]) {
                categories[menuCatId] = {
                    display_name: menuCatName || _t('Other'),
                    sequence: menuCatSeq,
                    value: menuCatId || 0,
                    menus: [],
                }
            }

            categories[menuCatId]['menus'].push(menu);
        });

        const categoryList = Object.keys(categories).map(key => categories[key]);
        categoryList.sort((a, b) => {
            if (a.sequence === undefined) {
                return 1;
            }

            if (b.sequence === undefined) {
                return -1;
            }

            return a.sequence - b.sequence;
        });

        return categoryList;
    },

    get rootMainAppSections() {
        const menus = [];

        this.rootMainCategoryAppSections.forEach((category) => {
            category.menus.forEach((menu) => {
                const newMenu = {...menu};
                newMenu.childrenTree = [];
                menus.push(newMenu);
            });
        });

        return menus;
    },
});
