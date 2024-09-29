/** @odoo-module **/

import {Component, onWillUpdateProps, useRef, useState} from '@odoo/owl';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {usePopover} from '@web/core/popover/popover_hook';
import {useBus, useService} from '@web/core/utils/hooks';
import {findFirstSelectableMenu} from '@pyper/webclient/menus/menu_helpers';
import {DrawerPopoverItem} from './drawer_popover_item';


export class DrawerMenuItem extends Component {
    static template = 'pyper_drawer.DrawerMenuItem';

    static components = {
        DropdownItem: DropdownItem,
        DrawerMenuItem: DrawerMenuItem,
    };

    static props = {
        menuXmlid: {
            type: String,
            optional: true,
        },
        menuId: {
            type: [Number, String],
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
        childrenDepth: {
            type: Number,
            optional: true,
        },
        children: {
            type: Array,
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
        depth: {
            type: Number,
            optional: true,
        }
    }

    static defaultProps = {
        childrenDepth: 0,
        children: [],
        withIcon: false,
        active: undefined,
        depth: 0,
    }

    setup() {
        this.drawerService = useState(useService('drawer'));
        this.menuStateService = useState(useService('menu_state'));
        this.actionService = useService('action');
        this.menuService = useService('menu');
        this.content = useRef('content');
        this.state = useState({
            opened: this.menuStateService.menuIsActivated(this.props.menuId),
        });

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

        useBus(this.env.bus, 'MENU-STATE:MENU-SELECTED', this.onMenuItemSelected.bind(this));
        useBus(this.env.bus, 'DRAWER:OPEN-MENU', this.onMenuItemOpened.bind(this));
    }

    get classes() {
        return {
            'o_drawer--menu-item': true,
            'o_drawer--menu-item-active': this.isActive,
            'o_drawer--menu-item-opened': this.isOpened,
        };
    }

    get styles() {
        return {
            '--drawer-item-depth': this.props.depth,
        };
    }

    get hasChildren() {
        return this.props.childrenDepth !== 0 && this.props.children.length > 0;
    }

    get displayChildren() {
        return this.hasChildren && this.props.children.length > 1;
    }

    get displayIcon() {
        return this.props.withIcon || !!this.props.fontIcon;
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

    get isActive() {
        if (undefined === this.props.active) {
            return this.menuStateService.activeIds.includes(this.props.menuId);
        }

        return this.props.active;
    }

    get isOpened() {
        return this.state.opened;
    }

    get childrenDepth() {
        return this.props.childrenDepth < 0 ? -1 : Math.max(0, this.props.childrenDepth - 1);
    }

    toggleChildren() {
        this.setOpened(!this.state.opened);
    }

    setOpened(opened) {
        this.state.opened = this.displayChildren ? !!opened : false;

        if (this.state.opened && this.props.menuId && this.drawerService.closeAllUnactivatedItemsOnOpenMenu) {
            this.drawerService.openMenu(this.menuService.getMenu(this.props.menuId));
        }
    }

    onItemSelection() {
        if (this.displayChildren && !this.isPopoverEnabled) {
            this.toggleChildren();
        } else if (this.props.menuId) {
            // Check if action is external identifier of menu
            let menu = undefined;

            if (typeof this.props.menuId === 'string') {
                menu = this.menuService.getAll().find((item) => item.xmlid === this.props.menuId);
            }

            if (!menu) {
                menu = this.menuService.getMenu(this.props.menuId);
            }

            // Force to find first sub menu item with action id
            if (menu && menu.childrenTree.length > 0) {
                menu = findFirstSelectableMenu(menu.childrenTree);
            }

            this.drawerService.selectMenu(menu);
        } else if (this.props.menuAction) {
            this.actionService.doAction(this.props.menuAction, {
                clearBreadcrumbs: true,
            }).then();
        }
    }

    onMenuItemOpened(e) {
        if (this.state.opened && this.drawerService.closeAllUnactivatedItemsOnOpenMenu && !e.detail.ids.includes(this.props.menuId)) {
            this.setOpened(false);
        }
    }

    onMenuItemSelected() {
        if (this.drawerService.closeAllUnactivatedItemsOnClick) {
            this.setOpened(this.menuStateService.menuIsActivated(this.props.menuId));
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
                displayIcon: false,
                onItemMouseEnter: this.onItemMouseEnter.bind(this),
                onItemMouseLeave: this.onItemMouseLeave.bind(this),
                onItemSelection: this.onItemSelection.bind(this),
                menuItemHref: this.menuItemHref,
            });
        }
    }
}
