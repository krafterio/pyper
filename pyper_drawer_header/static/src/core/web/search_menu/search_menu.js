/* @odoo-module */

import {Component} from '@odoo/owl';

import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';
import {isMacOS} from '@web/core/browser/feature_detection';

export class SearchMenu extends Component {
    static template = 'pyper_drawer_header.SearchMenu';

    static props = {};

    setup() {
        this.command = useService('command');
    }

    get tooltip() {
        return `${isMacOS() ? 'CMD' : 'CTRL'}+K`;
    }

    onClick() {
        this.command.openMainPalette({}, () => {});
    }
}

registry
    .category('drawer_header')
    .add('pyper_drawer_header.SearchMenu', {Component: SearchMenu}, {sequence: 3})
;
