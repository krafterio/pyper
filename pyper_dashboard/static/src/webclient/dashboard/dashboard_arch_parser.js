/** @odoo-module **/

import {makeContext} from '@web/core/context';
import {Domain} from '@web/core/domain';
import {visitXML} from '@web/core/utils/xml';
import {_t} from '@web/core/l10n/translation';
import {getActiveActions} from '@web/views/utils';
import {exprToBoolean} from '@web/core/utils/strings';

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
                    archInfo.useSwitcher = exprToBoolean(node.getAttribute('switcher'), true);
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
                    let selectedColumn = archInfo.sections[currentSectionIdx]?.columns[currentColumnIdx];

                    // Use the last available section and last available column if current section does not exist
                    if (!selectedColumn) {
                        const selectedSection = archInfo.sections[archInfo.sections.length - 1]
                        selectedColumn = selectedSection.columns[selectedSection.columns.length - 1];
                    }

                    selectedColumn?.actions?.push(action);
                    break;
                }
                default:
                    if (!hasDashboard) {
                        throw new DashboardArchParserError(_t('The "dashboard" tag must be the only one child element of "form" tag. You cannot add other tags in the "form" tag if "dashboard" is used'));
                    }
                    break;
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
        exprToBoolean(node.getAttribute('layout_editable'), true),
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

    const hasActionId = actionId !== undefined && actionId !== null;
    const type = hasActionId ? 'action' : (node.getAttribute('type') || 'action');

    const action = {
        id,
        type,
        actionId: hasActionId ? actionId : undefined,
        resModel: !hasActionId ? (node.getAttribute('model') || undefined) : undefined,
        title: node.getAttribute('string') || undefined,
        icon: node.getAttribute('icon') || undefined,
        viewMode: node.getAttribute('view_mode') || undefined,
        context: {},
        domain: [],
        isFolded: exprToBoolean(node.getAttribute('fold')),
        height: node.getAttribute('height') || undefined,
        minHeight: node.getAttribute('min_height') || undefined,
        maxHeight: node.getAttribute('max_height') || undefined,
    };

    if (node.hasAttribute('context') && node.getAttribute('context')) {
        action.context = makeContext([node.getAttribute('context')]);
    }

    if (node.hasAttribute('domain') && node.getAttribute('domain')) {
        action.domain = new Domain(node.getAttribute('domain')).toList({});
    }

    // So it can be serialized when reexporting dashboard xml
    action.context.toString = () => node.getAttribute('context');
    action.domain.toString = () => node.getAttribute('domain');

    action.filterField = node.getAttribute('filter_field') || undefined;
    action.filterFieldType = node.getAttribute('filter_field_type') || undefined;

    return action;
}

/**
 * @param {*} value
 * @returns {String}
 */
export const serializePythonValue = function(value) {
    if (typeof value === 'string') return `'${value}'`;
    if (typeof value === 'boolean') return value ? 'True' : 'False';
    if (typeof value === 'number') return String(value);
    if (Array.isArray(value)) return `[${value.map(serializePythonValue).join(', ')}]`;
    if (value === null || value === undefined) return 'None';
    if (typeof value === 'object') return serializePythonDict(value);
    return String(value);
};

/**
 * @param {Object} obj
 * @returns {String}
 */
export const serializePythonDict = function(obj) {
    const entries = Object.entries(obj)
        .filter(([k]) => !k.startsWith('_') && k !== 'toString')
        .map(([k, v]) => `'${k}': ${serializePythonValue(v)}`);
    return entries.length ? `{${entries.join(', ')}}` : '';
};

/**
 * @param {Number} id
 * @param {Object} data
 * @returns {Object}
 */
export const createActionData = function(id, data) {
    const hasActionId = !!data.actionId;
    const action = {
        id,
        type: hasActionId ? 'action' : (data.type || 'view'),
        actionId: hasActionId ? data.actionId : undefined,
        resModel: !hasActionId ? data.resModel : undefined,
        title: data.title || undefined,
        icon: data.icon || undefined,
        viewMode: data.viewMode || undefined,
        context: data.context || {},
        domain: data.domain || [],
        isFolded: false,
        height: data.height || undefined,
        minHeight: data.minHeight || undefined,
        maxHeight: data.maxHeight || undefined,
        filterField: data.filterField || undefined,
        filterFieldType: data.filterFieldType || undefined,
    };

    const contextStr = Object.keys(action.context).length > 0
        ? serializePythonDict(action.context)
        : '';
    action.context.toString = () => contextStr;
    action.domain.toString = () => action.domain.length > 0
        ? JSON.stringify(action.domain) : '';

    return action;
};
