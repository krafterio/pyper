/** @odoo-module **/

import {Domain} from '@web/core/domain';
import {visitXML} from '@web/core/utils/xml';
import {archParseBoolean} from '@web/views/utils';

export class DashboardArchParser {
    parse(arch, customViewId) {
        let nextId = 1;
        const archInfo = {
            title: null,
            layout: null,
            useSwitcher: false,
            colNumber: 0,
            isEmpty: true,
            columns: [
                {actions: []},
                {actions: []},
                {actions: []},
            ],
            customViewId,
        };
        let currentIndex = -1;

        visitXML(arch, (node) => {
            switch (node.tagName) {
                case 'form':
                    archInfo.title = node.getAttribute('string');
                    break;
                case 'dashboard':
                    archInfo.layout = node.getAttribute('layout');
                    archInfo.useSwitcher = archParseBoolean(node.getAttribute('switcher'), true);
                    archInfo.colNumber = archInfo.layout.split('-').length;
                    break;
                case 'column':
                    currentIndex++;
                    break;
                case 'action': {
                    archInfo.isEmpty = false;
                    const action = {
                        id: nextId++,
                        title: node.getAttribute('string'),
                        actionId: parseInt(node.getAttribute('name'), 10),
                        viewMode: node.getAttribute('view_mode'),
                        context: node.getAttribute('context'),
                        isFolded: archParseBoolean(node.getAttribute('fold')),
                    };

                    if (node.hasAttribute('domain')) {
                        const domain = node.getAttribute('domain');
                        action.domain = new Domain(domain).toList({});
                        // so it can be serialized when reexporting dashboard xml
                        action.domain.toString = () => node.getAttribute('domain');
                    }

                    archInfo.columns[currentIndex].actions.push(action);
                    break;
                }
            }
        });

        return archInfo;
    }
}
