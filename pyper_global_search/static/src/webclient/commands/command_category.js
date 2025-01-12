/** @odoo-module **/

import {registry} from '@web/core/registry';

const commandCategoryRegistry = registry.category('command_categories');
// displays the records on input "!"
commandCategoryRegistry.add('global_search_records', {namespace: '>'}, {sequence: 1});
