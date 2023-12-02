/** @odoo-module */

import {registry} from '@web/core/registry';
import '@web/webclient/menus/menu_providers'

const commandProviderRegistry = registry.category('command_provider');
const menu = commandProviderRegistry.get('menu');
const menuProvideFct = menu.provide;

menu.provide = async function (env, options) {
    const menuService = env.services.menu;
    const res = await menuProvideFct(env, options);

    res.forEach((item) => {
        const usp = new URLSearchParams(item.href.replace('#', ''));
        const menuId = usp.get('menu_id');

        if (menuId) {
            const menu = menuService.getMenu(menuId);

            if (menu.font_icon || menu.font_icon_color) {
                item.props.webIcon = {
                    iconClass: menu.font_icon,
                    color: menu.font_icon_color,
                    backgroundColor: undefined,
                };
                delete item.props.webIconData;
            }
        }
    });

    return res;
};
