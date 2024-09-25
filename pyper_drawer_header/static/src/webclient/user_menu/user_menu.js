/** @odoo-module **/

import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { Component } from "@odoo/owl";

const userMenuRegistry = registry.category("user_menuitems");

export class DrawerUserMenu extends Component {
    setup() {
        this.user = useService("user");
        const { origin } = browser.location;
        const { userId } = this.user;
        this.source = `${origin}/web/image?model=res.users&field=avatar_128&id=${userId}`;
    }

    getElements() {
        const sortedItems = userMenuRegistry
            .getAll()
            .map((element) => element(this.env))
            .sort((x, y) => {
                const xSeq = x.sequence ? x.sequence : 100;
                const ySeq = y.sequence ? y.sequence : 100;
                return xSeq - ySeq;
            });
        return sortedItems;
    }
}
DrawerUserMenu.template = "pyper_drawer_header.UserMenu";
DrawerUserMenu.components = { Dropdown, DropdownItem, CheckBox };
DrawerUserMenu.props = {};

export const pyperDrawerUserItem = {
    Component: DrawerUserMenu,
};

registry.category("drawer_header").add("pyper_drawer_header.drawer_user_menu", pyperDrawerUserItem, { sequence: 1 });
