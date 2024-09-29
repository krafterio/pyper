/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {cookie} from '@web/core/browser/cookie';
import {registry} from '@web/core/registry';
import {SIZES} from '@web/core/ui/ui_service';


export class DrawerState {
    constructor(envBus, ui) {
        this.envBus = envBus;
        /** @type {import("@web/core/ui/ui_service").uiService} */
        this.uiService = ui;
    }

    setup() {
        this.state = {
            nav: false,
            fixedTop: false,
            opened: false,
            locked: (cookie.get('drawer_locked') || 'true') === 'true',
            lockable: false,
            minifiable: false,
            minified: false,
            alwaysMinified: false,
            popoverMinified: false,
            disabledOnSmallScreen: false,
            dragging: false,
            mounted: false,
            closeAllUnactivatedItemsOnClick: false,
        };
    }

    get nav() {
        return this.state.nav;
    }

    set nav(nav) {
        this.state.nav = nav;
    }

    get fixedTop() {
        return this.state.fixedTop;
    }

    set fixedTop(fixedTop) {
        this.state.fixedTop = fixedTop;
    }

    get opened() {
        return this.state.opened;
    }

    set opened(opened) {
        this.state.opened = opened;
    }

    get locked() {
        return this.state.locked;
    }

    set locked(locked) {
        this.state.locked = locked;
        cookie.set('drawer_locked', locked);
    }

    get lockable() {
        return this.state.lockable;
    }

    set lockable(lockable) {
        this.state.lockable = lockable;
    }

    get minifiable() {
        return this.state.minifiable;
    }

    set minifiable(minifiable) {
        this.state.minifiable = minifiable;
    }

    get minified() {
        return this.state.minified;
    }

    set minified(minified) {
        this.state.minified = minified;
        cookie.set('drawer_minified', minified);
    }

    get alwaysMinified() {
        return this.state.alwaysMinified;
    }

    set alwaysMinified(alwaysMinified) {
        this.state.alwaysMinified = alwaysMinified;
    }

    get popoverMinified() {
        return this.state.popoverMinified;
    }

    set popoverMinified(popoverMinified) {
        this.state.popoverMinified = popoverMinified;
    }

    get disabledOnSmallScreen() {
        return this.state.disabledOnSmallScreen;
    }

    set disabledOnSmallScreen(disabledOnSmallScreen) {
        this.state.disabledOnSmallScreen = disabledOnSmallScreen;
    }

    get dragging() {
        return this.state.dragging;
    }

    set dragging(dragging) {
        this.state.dragging = dragging;
    }

    get mounted() {
        return this.state.mounted;
    }

    set mounted(mounted) {
        this.state.mounted = mounted;
    }

    get isSmallScreen() {
        return this.uiService.size <= SIZES.LG;
    }

    get isNav() {
        return this.nav;
    }

    get isLockable() {
        return this.lockable;
    }

    get isLocked() {
        return this.locked && this.isLockable && !this.isSmallScreen;
    }

    get isMinifiable() {
        return this.minifiable || this.alwaysMinified;
    }

    get isMinified() {
        return (this.minified || this.alwaysMinified) && this.isMinifiable && !this.isSmallScreen;
    }

    get isPopoverMinified() {
        return this.isMinified && this.popoverMinified;
    }

    get isHoverable() {
        return this.isSmallScreen || !this.locked;
    }

    get isDraggable() {
        return this.isHoverable;
    }

    get isOpened() {
        return this.opened;
    }

    get isClosed() {
        return !this.opened;
    }

    get isClosable() {
        return !this.isLocked && this.opened;
    }

    get isFixedTop() {
        return this.fixedTop && !this.isSmallScreen;
    }

    get popover() {
        return this._popover;
    }

    set popover(popover) {
        this._popover = popover;
    }

    get closeAllUnactivatedItemsOnClick() {
        return this.state.closeAllUnactivatedItemsOnClick;
    }

    set closeAllUnactivatedItemsOnClick(value) {
        this.state.closeAllUnactivatedItemsOnClick = value;
    }

    restoreMinified(defaultMinified) {
        defaultMinified = !(defaultMinified in [undefined, 'false', false]);
        const defaultValue = defaultMinified ? 'true' : 'false';
        const minified = (cookie.get('drawer_minified') || defaultValue) === 'true';

        this.state.minified = minified;

        return minified;
    }

    toggle() {
        this.envBus.trigger('DRAWER:TOGGLE');
    }

    selectMenu(menu) {
        this.envBus.trigger('DRAWER:SELECT-MENU', menu);
    }
}

export const drawerService = {
    dependencies: ['ui'],
    start(env, {ui}) {
        const drawerState = reactive(new DrawerState(env.bus, ui));
        drawerState.setup();

        return drawerState;
    },
};

registry.category('services').add('drawer', drawerService);
