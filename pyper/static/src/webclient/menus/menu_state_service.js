/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {registry} from '@web/core/registry';


export class MenuState {
    constructor(bus, menu) {
        /** @type {import("@bus/services/bus_service").busService} */
        this.bus = bus;
        /** @type {import("@web/webclient/menus/menu_service").menuService} */
        this.menuService = menu;
    }

    setup() {
        this.state = {
            currentMenuId: undefined,
        };
    }

    get currentMenuId() {
        return this.state.currentMenuId;
    }

    set currentMenuId(menuId) {
        this.state.currentMenuId = menuId;
        this.bus.trigger('MENU-STATE:MENU-SELECTED', menuId);
    }

    get activeIds() {
        return this.currentMenuId ? [...this.findParentIds(this.currentMenuId), this.currentMenuId] : [];
    }

    menuIsActivated(menu) {
        menu = typeof menu === 'number' ? this.menuService.getMenu(menu) : menu;

        return typeof menu === 'object' && this.activeIds.includes(menu.id);
    }

    findParentIds(targetMenuId) {
        if (!targetMenuId) {
            return [];
        }

        for (const menu of this.menuService.getAll()) {
            if (menu.id === targetMenuId) {
                return [...(menu['parentPath'] || [])];
            }
        }

        return [];
    }
}

export const menuStateService = {
    dependencies: ['menu'],
    start(env, {menu}) {
        const menuState = reactive(new MenuState(env.bus, menu));
        menuState.setup();

        return menuState;
    },
};

registry.category('services').add('menu_state', menuStateService);
