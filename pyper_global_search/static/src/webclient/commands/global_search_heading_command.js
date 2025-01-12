/** @odoo-module */

import {DefaultCommandItem} from '@web/core/commands/command_palette';

export class GlobalSearchHeadingCommand extends DefaultCommandItem {
    static template = 'pyper_global_search.GlobalSearchHeadingCommand';

    static props = {
        ...DefaultCommandItem.props,
        count: {
            type: Number,
            optional: true,
        }
    };
}
