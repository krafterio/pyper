/** @odoo-module **/

import {makeContext} from '@web/core/context';
import {Domain} from '@web/core/domain';
import {visitXML} from '@web/core/utils/xml';
import {_t} from '@web/core/l10n/translation';
import {archParseBoolean, getActiveActions} from '@web/views/utils';

export class DashboardArchParserError extends Error {}

export class DashboardArchParser {
    parse(arch, customViewId) {
        let nextId = 1;
        let hasDashboard = false;
        const archInfo = {
            title: null,
            useSwitcher: false,
            isEmpty: true,
            sections: [],
            activeActions: {
                type: 'view',
                edit: false,
                create: false,
                delete: false,
            },
            customViewId,
        };
        let currentSectionIdx = -1;
        let currentColumnIdx = -1;

        visitXML(arch, (node) => {
            switch (node.tagName) {
                case 'form':
                    archInfo.title = node.getAttribute('string');
                    break;
                case 'dashboard':
                    hasDashboard = true;
                    archInfo.title = node.getAttribute('string') || archInfo.title;
                    archInfo.useSwitcher = archParseBoolean(node.getAttribute('switcher'), true);
                    archInfo.activeActions = getActiveActions(node);
                    break;
                case 'section':
                    currentColumnIdx = -1; // Reset column index
                    currentSectionIdx++;
                    archInfo.sections.push(createSection(node));
                    break;
                case 'column':
                    if (-1 === currentSectionIdx) {
                        throw new DashboardArchParserError(_t('The "column" tag must be a child of "section" tag'));
                    }

                    currentColumnIdx++;
                    break;
                case 'action': {
                    if (-1 === currentSectionIdx || -1 === currentColumnIdx) {
                        throw new DashboardArchParserError(_t('The "action" tag must be a child of "column" and "section" tags'));
                    }

                    archInfo.isEmpty = false;
                    archInfo.sections[currentSectionIdx].isEmpty = false;

                    const action = createAction(nextId++, node);
                    archInfo.sections[currentSectionIdx].columns[currentColumnIdx].actions.push(action);
                    break;
                }
                default:
                    if (!hasDashboard) {
                        throw new DashboardArchParserError(_t('The "dashboard" tag must be the only one child element of "form" tag. You cannot add other tags in the "form" tag if "dashboard" is used'));
                    }
                    break
            }
        });

        return archInfo;
    }
}

/**
 * @param {Element} node
 *
 * @return {Object}
 */
export const createSection = function(node) {
    return createSectionData(
        node.getAttribute('layout') || '1',
        archParseBoolean(node.getAttribute('layout_editable'), true),
        node.getAttribute('string') || undefined,
    );
}

/**
 *
 * @param {String}      layout
 * @param {Boolean}     layoutEditable
 * @param {String|null} title
 *
 * @return {Object}
 */
export const createSectionData = function(layout, layoutEditable, title) {
    const columnNumber = layout.split('-').length;

    return {
        title,
        layout,
        columnNumber,
        layoutEditable,
        isEmpty: true,
        columns: [
            ...Array.from({length: columnNumber}, () => createColumnData()),
        ],
    };
}

/**
 * @return {Object}
 */
export const createColumnData = function() {
    return {
        actions: [],
    };
}

/**
 *
 * @param {Number}  id
 * @param {Element} node
 *
 * @return Object
 */
export const createAction = function(id, node) {
    let actionId = node.getAttribute('name');
    const actionIdInt = parseInt(actionId, 10);

    if (!isNaN(actionIdInt)) {
        actionId = actionIdInt;
    }

    const action = {
        id,
        actionId,
        title: node.getAttribute('string'),
        viewMode: node.getAttribute('view_mode'),
        context: {},
        domain: [],
        isFolded: archParseBoolean(node.getAttribute('fold')),
    };

    if (node.hasAttribute('context')) {
        action.context = makeContext([node.getAttribute('context')]);
    }

    if (node.hasAttribute('domain')) {
        action.domain = new Domain(node.getAttribute('domain')).toList({});
    }

    // So it can be serialized when reexporting dashboard xml
    action.context.toString = () => node.getAttribute('context');
    action.domain.toString = () => node.getAttribute('domain');

    return action;
}
