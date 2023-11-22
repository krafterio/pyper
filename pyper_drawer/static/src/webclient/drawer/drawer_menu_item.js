/** @odoo-module **/

import {Component, onWillUpdateProps, useRef, useState} from '@odoo/owl';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {usePopover} from '@web/core/popover/popover_hook';
import {useService} from '@web/core/utils/hooks';
import {DrawerPopoverItem} from './drawer_popover_item';


export class DrawerMenuItem extends Component {
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
        active: {
            type: Boolean,
            optional: true,
        },
    }

    static defaultProps = {
        withIcon: false,
        active: false,
    }

    setup() {
        this.drawerService = useState(useService('drawer'));
        this.actionService = useService('action');
        this.content = useRef('content');

        if (!this.drawerService.popover) {
            const navCls = (this.drawerService.isNav ? ' o_drawer--popover-item-nav' : '');
            this.drawerService.popover = usePopover(DrawerPopoverItem, {
                position: 'right-middle',
                animation: false,
                arrow: false,
                fixedPosition: false,
                popoverClass: 'o_drawer--popover-item' + navCls,
            });
        }

        onWillUpdateProps((nextProps) => this.onWillUpdateProps(nextProps));
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
        if (this.props.menuId) {
            this.drawerService.selectMenu(this.props.menuId);
        } else if (this.props.menuAction) {
            this.actionService.doAction(this.props.menuAction, {
                clearBreadcrumbs: true,
            }).then();
        }
    }

    onItemMouseEnter() {
        this.openPopover();
    }

    onItemMouseLeave() {
        this.drawerService.popover.close();
    }

    onWillUpdateProps(nextProps) {
        if (nextProps.active && this.drawerService.popover.isOpen) {
            this.openPopover(nextProps);
        }
    }

    openPopover(props) {
        if (this.isPopoverEnabled) {
            this.drawerService.popover.open(this.content.el, {
                ...this.props,
                ...(props || {}),
                withIcon: false,
                onItemMouseEnter: this.onItemMouseEnter.bind(this),
                onItemMouseLeave: this.onItemMouseLeave.bind(this),
                onItemSelection: this.onItemSelection.bind(this),
                menuItemHref: this.menuItemHref,
            });
        }
    }
}
