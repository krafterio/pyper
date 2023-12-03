/* @odoo-module */

import {Component} from '@odoo/owl';

import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';
import {isMacOS} from '@web/core/browser/feature_detection';

export class SearchMenu extends Component {
    static template = 'pyper_command_search.SearchMenu';

    static components = {
        DropdownItem,
    };

    static props = {};

    setup() {
        this.command = useService('command');
    }

    get tooltip() {
        return `${isMacOS() ? 'CMD' : 'CTRL'}+K`;
    }

    onSelected() {
        this.command.openMainPalette({}, () => {});
    }
}

registry
    .category('systray')
    .add('pyper_command_search.search_menu', {Component: SearchMenu}, {sequence: 100})
;
