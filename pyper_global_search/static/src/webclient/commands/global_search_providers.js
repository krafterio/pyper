/** @odoo-module */

import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {GlobalSearchRecordCommand} from './global_search_record_command';
import {GlobalSearchHeadingCommand} from './global_search_heading_command';
import {GlobalSearchInfoCommand} from './global_search_info_command';

const commandSetupRegistry = registry.category('command_setup');
const commandProviderRegistry = registry.category('command_provider');

// Command setup
commandSetupRegistry.add('>', {
    debounceDelay: 500,
    emptyMessage: _t('No record found.'),
    name: _t('records'),
    placeholder: _t('Search a record...'),
});

const fn = () => {
    let recordsData;

    return async function provide(env, options) {
        if (!options.searchValue) {
            return [{
                category: 'global_search_records',
                name: _t('Quickly search records in all available models'),
                Component: GlobalSearchInfoCommand,
                action: () => {},
            }];
        }

        recordsData = await env.services.rpc('/web/global-search', {search_value: options.searchValue});

        if (recordsData.length === 0) {
            return [];
        }

        const result = [];

        recordsData.results.forEach((modelSection) => {
            result.push({
                category: 'global_search_records',
                name: modelSection.name || _t('Untitled'),
                Component: GlobalSearchHeadingCommand,
                props: {
                    count: modelSection.count,
                },
                action: async () => {
                    const action = await env.services.action.loadAction(modelSection.actionId, {});
                    const viewModes = action.view_mode.split(',').map((view) => view.trim());

                    env.services.action.doAction({
                            ...action,
                            domain: modelSection.searchDomain || action.domain,
                        }, {
                            viewType: viewModes.includes('list') ? 'list' : viewModes?.[0],
                        });
                },
            });

            modelSection.items.forEach((item) => {
                result.push({
                    category: 'global_search_records',
                    name: item.display_name || _t('Untitled'),
                    Component: GlobalSearchRecordCommand,
                    props: {},
                    action: async () => {
                        const action = await env.services.action.loadAction(modelSection.actionId, {});
                        env.services.action.doAction({
                            ...action,
                            res_id: item.id,
                        }, {
                            viewType: 'form',
                        });
                    },
                });
            });
        });

        return result;
    };
};

commandProviderRegistry.add('global_search', {
    debounceDelay: 500,
    namespace: '>',
    provide: fn(),
});
