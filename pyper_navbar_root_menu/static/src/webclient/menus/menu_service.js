/** @odoo-module **/

import {menuService} from '@web/webclient/menus/menu_service';

const originalStart = menuService.start;

menuService.start = async function (env) {
    const resStart = await originalStart(env);
    const originalSelectMenu = resStart.selectMenu.bind(resStart);
    const originalSetCurrentMenu = resStart.setCurrentMenu.bind(resStart);

    resStart.currentMenuId = undefined;

    resStart.selectMenu = async function (menu) {
        resStart.currentMenuId = typeof menu === 'number' ? menu : menu.id;
        await originalSelectMenu(menu);
    };

    resStart.setCurrentMenu = function (menu) {
        resStart.currentMenuId = typeof menu === 'number' ? menu : menu.id;
        originalSetCurrentMenu(menu);
    };

    return resStart;
};
