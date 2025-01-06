/** @odoo-module **/

import {menuService} from '@web/webclient/menus/menu_service';

const originalStart = menuService.start;

menuService.start = async function (env) {
    const resStart = await originalStart(env);

    env.services.bus_service.subscribe('user_menu_collection_changed', async () => {
        await resStart.reload();
        env.bus.trigger('MENUS-COUNTER:LOAD');
    });

    env.services.bus_service.subscribe('user_menu_collection_items_changed', async () => {
        env.bus.trigger('MENUS-COUNTER:LOAD');
    });

    return resStart;
};
