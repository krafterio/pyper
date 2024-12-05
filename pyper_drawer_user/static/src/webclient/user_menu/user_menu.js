/** @odoo-module **/

import { registry } from "@web/core/registry";

const systrayUserMenu = registry.category('systray').get('web.user_menu');

registry.category('systray').remove('web.user_menu');
registry.category('drawer_user').add("pyper_drawer_user.drawer_user_menu", systrayUserMenu, {sequence: 1});
