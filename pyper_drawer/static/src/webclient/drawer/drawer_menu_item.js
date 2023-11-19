/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {usePopover} from '@web/core/popover/popover_hook';
import {useService} from '@web/core/utils/hooks';
import {DrawerPopoverItem} from './drawer_popover_item';


export class DrawerMenuItem extends Component {
    static description = 'Menu item of Drawer';

    static template = 'pyper_drawer.DrawerMenuItem';

    static components = {
        DropdownItem: DropdownItem,
    };

    static props = {
        menuXmlid: {
            type: String,
            optional: true,
        },
        menuId: {
            type: Number,
            optional: true,
        },
        menuAction: {
            type: [String, Number],
            optional: true,
        },
        hotkey: {
            type: String,
            optional: true,
        },
        withIcon: {
            type: Boolean,
            optional: true,
        },
        iconData: {
            type: String,
            optional: true,
        },
        fontIcon: {
            type: String,
            optional: true,
        },
        fontIconColor: {
            type: String,
            optional: true,
        },
        label: {
            type: String,
            optional: true,
        },
    }

    static defaultProps = {
        withIcon: false,
    }

    setup() {
        this.drawerService = useState(useService('drawer'));

        if (!this.drawerService.popover) {
            this.drawerService.popover = usePopover(DrawerPopoverItem, {
                position: 'left-start',
                animation: false,
                arrow: false,
                fixedPosition: true,
                popoverClass: 'o_drawer--popover-item',
            });
        }
    }

    get isPopoverEnabled() {
        return this.drawerService.isMinified && this.drawerService.popoverMinified;
    }

    get menuItemHref() {
        if (!this.props.menuId && !this.props.menuAction) {
            return undefined;
        }

        const parts = [];

        if (this.props.menuId) {
            parts.push(`menu_id=${this.props.menuId}`);
        }

        if (this.props.menuAction) {
            parts.push(`action=${this.props.menuAction}`);
        }

        return '#' + parts.join('&');
    }

    onItemSelection() {
        this.drawerService.selectMenu(this.props.menuId);
    }

    onItemMouseEnter(evt) {
        if (this.isPopoverEnabled) {
            this.drawerService.popover.open(evt.toElement, {
                ...this.props,
                onItemMouseEnter: this.onItemMouseEnter.bind(this),
                onItemMouseLeave: this.onItemMouseLeave.bind(this),
                onItemSelection: this.onItemSelection.bind(this),
                menuItemHref: this.menuItemHref,
            });
        }
    }

    onItemMouseLeave() {
        this.drawerService.popover.close();
    }
}
