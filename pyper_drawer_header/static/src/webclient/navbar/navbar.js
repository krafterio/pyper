/** @odoo-module **/

import { NavBar } from '@web/webclient/navbar/navbar';
import { patch } from '@web/core/utils/patch';
import { registry } from "@web/core/registry";


const headerDrawerRegistry = registry.category("drawer_header");
const headerDrawerActionRegistry = registry.category("drawer_header_action");

patch(NavBar.prototype, {
    setup() {
        super.setup();
    },

    get headerDrawerItems() {
        return headerDrawerRegistry
            .getEntries()
            .map(([key, value]) => ({ key, ...value }))
            .filter((item) => ("isDisplayed" in item ? item.isDisplayed(this.env) : true))
    },

    get headerDrawerActionItems() {
        return headerDrawerActionRegistry
            .getEntries()
            .map(([key, value]) => ({ key, ...value }))
            .filter((item) => ("isDisplayed" in item ? item.isDisplayed(this.env) : true))
    },

});

NavBar.components.drawerHeader = NavBar.prototype.getDrawerHeader;
NavBar.components.drawerHeaderAction = NavBar.prototype.getDrawerHeaderAction;