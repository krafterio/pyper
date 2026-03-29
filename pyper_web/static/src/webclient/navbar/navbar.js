/** @odoo-module **/

import {useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {patch} from '@web/core/utils/patch';
import {OverlayMenuToggler} from '../overlay_menu/overlay_menu_toggler';
import {NavBar} from '@web/webclient/navbar/navbar';

NavBar.components.OverlayMenuToggler = OverlayMenuToggler;

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        this.overlayMenuService = useState(useService('overlay_menu'));
    },
    onAllAppsBtnClick() {
        this._closeAppMenuSidebar();
        this.overlayMenuService.toggle();
    },
});
