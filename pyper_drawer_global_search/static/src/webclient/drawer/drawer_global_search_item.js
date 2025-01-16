/* @odoo-module */

import {Component, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {DrawerMenuItem} from '@pyper_drawer/webclient/drawer/drawer_menu_item';
import {GlobalSearchInput} from '@pyper_global_search/webclient/global_search/global_search_input';


export class DrawerGlobalSearchItem extends Component {
    static template = 'pyper_drawer_global_search.DrawerGlobalSearchItem';

    static components = {
        GlobalSearchInput,
        DrawerMenuItem,
    };

    static props = {};

    setup() {
        this.drawerService = useState(useService('drawer'));
    }

    get isMinified() {
        return this.drawerService.isMinified;
    }

    get fontIcon() {
        return 'fa fa-search';
    }
}
