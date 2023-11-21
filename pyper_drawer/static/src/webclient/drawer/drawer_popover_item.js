/** @odoo-module **/

import {Component} from '@odoo/owl';

export class DrawerPopoverItem extends Component {
    static template = 'pyper_drawer.DrawerPopoverItem';

    static props = {
        '*': {optional: true},
    };
}
