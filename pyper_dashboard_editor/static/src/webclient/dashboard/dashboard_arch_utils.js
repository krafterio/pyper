/** @odoo-module **/

import {blockDom} from '@odoo/owl';
import {renderToString} from '@web/core/utils/render';

const xmlSerializer = new XMLSerializer();

/**
 * @param {Object} data - Dashboard-like data object
 * @returns {String}
 */
export const renderDashboardArch = function(data) {
    const templateFn = renderToString.app.getTemplate('pyper_dashboard_editor.Arch');
    const bdom = templateFn(data, {});
    const root = document.createElement('rendertostring');
    blockDom.mount(bdom, root);
    const result = xmlSerializer.serializeToString(root);

    return result.slice(result.indexOf('<', 1), result.indexOf('</rendertostring>'));
};

/**
 * @param {Object} action
 * @returns {String}
 */
export const renderActionArch = function(action) {
    const arch = renderDashboardArch({
        title: '',
        useSwitcher: false,
        sections: [{
            layout: '1',
            columnNumber: 1,
            layoutEditable: true,
            columns: [{actions: [action]}],
        }],
    });

    const match = arch.match(/<action\b[^]*?\/>/);

    return formatXml(match ? match[0] : arch);
};

/**
 * @param {Object} section
 * @returns {String}
 */
export const renderSectionArch = function(section) {
    const arch = renderDashboardArch({
        title: '',
        useSwitcher: false,
        sections: [section],
    });

    const match = arch.match(/<section\b[^]*?<\/section>/);

    return formatXml(match ? match[0] : arch);
};

const formatXml = function(xml) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'text/xml');

    if (doc.querySelector('parsererror')) {
        return xml;
    }

    return serializeNode(doc.documentElement, 0);
};

const serializeNode = function(node, depth) {
    const indent = '    '.repeat(depth);

    if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent.trim();

        return text ? indent + text : '';
    }

    const attrs = [];

    for (const attr of node.attributes || []) {
        attrs.push(`${attr.name}="${attr.value}"`);
    }

    const tag = node.tagName;
    const attrStr = attrs.length ? ' ' + attrs.join(' ') : '';
    const children = [...node.childNodes].map((c) => serializeNode(c, depth + 1)).filter(Boolean);

    if (!children.length) {
        return `${indent}<${tag}${attrStr}/>`;
    }

    return `${indent}<${tag}${attrStr}>\n${children.join('\n')}\n${indent}</${tag}>`;
};
