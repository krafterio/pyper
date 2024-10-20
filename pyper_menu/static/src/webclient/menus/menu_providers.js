/** @odoo-module */

import {registry} from '@web/core/registry';
import '@web/webclient/menus/menu_providers'

const commandProviderRegistry = registry.category('command_provider');
const menu = commandProviderRegistry.get('menu');
const menuProvideFct = menu.provide;

const MENU_SETUP_PREFIX = 'pyper_menu.provider.';

menu.provide = async function (env, options) {
    const menuService = env.services.menu;
    const pyperSetupService = env.services['pyper_setup'];
    const res = await menuProvideFct(env, options);

    await pyperSetupService.register(MENU_SETUP_PREFIX, {
        preferWebIcon: false,
    });

    res.forEach((item) => {
        const usp = new URLSearchParams(item.href.replace('#', ''));
        const menuId = usp.get('menu_id');

        if (menuId) {
            const menu = menuService.getMenu(menuId);

            if ((menu.font_icon || menu.font_icon_color) && item.props) {
                item.props.webIcon = {
                    iconClass: menu.font_icon,
                    color: menu.font_icon_color,
                    backgroundColor: undefined,
                };

                if (!pyperSetupService.settings[MENU_SETUP_PREFIX].preferWebIcon) {
                    delete item.props.webIconData;
                }
            }
        }
    });

    return res;
};
