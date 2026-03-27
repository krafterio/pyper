/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {registry} from '@web/core/registry';


export class OverlayMenuService {
    constructor(envBus, ui) {
        this.envBus = envBus;
        /** @type {import("@web/core/ui/ui_service").uiService} */
        this.uiService = ui;
    }

    setup() {
        this.state = {
            mounted: false,
            opened: false,
        };
    }

    get mounted() {
        return this.state.mounted;
    }

    set mounted(mounted) {
        this.state.mounted = mounted;
    }

    get opened() {
        return this.state.opened;
    }

    set opened(opened) {
        this.state.opened = opened;
    }

    get isOpened() {
        return this.opened;
    }

    get isClosed() {
        return !this.opened;
    }

    toggle() {
        this.envBus.trigger('OVERLAY-MENU:TOGGLE');
    }

    selectMenu(menu) {
        this.envBus.trigger('OVERLAY-MENU:SELECT-MENU', menu);
    }
}

export const overlayMenuService = {
    dependencies: ['ui'],
    start(env, {ui}) {
        const overlayMenuService = reactive(new OverlayMenuService(env.bus, ui));
        overlayMenuService.setup();

        return overlayMenuService;
    },
};

registry.category('services').add('overlay_menu', overlayMenuService);
