/** @odoo-module **/

import {browser} from '@web/core/browser/browser';
import {visitXML} from '@web/core/utils/xml';
import {getGroupBy} from '@web/search/utils/group_by';
import {stringToOrderBy} from '@web/search/utils/order_by';
import {Field} from '@web/views/fields/field';
import {archParseBoolean, getActiveActions} from '@web/views/utils';
import {Widget} from '@web/views/widgets/widget';
import {AVAILABLE_SCALES} from './timeline_controller';

export class TimelineParseArchError extends Error {}

export class TimelineArchParser {
    parse(arch, models, modelName) {
        const fields = models[modelName];
        const fieldNodes = {};
        const fieldNextIds = {};
        const widgetNodes = {};
        let widgetNextId = 0;
        const sessionScale = browser.sessionStorage.getItem('timeline-scale');
        let jsClass = null;
        let scales = [...AVAILABLE_SCALES];
        let scale = sessionScale || null;
        let activeActions = {};
        let formViewId = false;
        let zoomKey = 'ctrlKey';
        let zoomable = true;
        let limit = null;
        let fieldDateStart = null;
        let fieldDateEnd = null;
        let defaultGroupBy = ['id'];
        let defaultOrderBy = null;
        let itemTemplate = null;

        visitXML(arch, (node) => {
            switch (node.tagName) {
                case 'timeline':
                    if (!node.hasAttribute('field_date_start')) {
                        throw new TimelineParseArchError(
                            `Timeline view has not defined "field_date_start" attribute.`
                        );
                    }

                    activeActions = getActiveActions(node);
                    fieldDateStart = node.getAttribute('field_date_start');
                    fieldDateEnd = node.getAttribute('field_date_end');
                    jsClass = node.getAttribute('js_class');

                    if (node.hasAttribute('scales')) {
                        const scalesAttr = node.getAttribute('scales');
                        scales = scalesAttr.split(',').filter((scale) => AVAILABLE_SCALES.includes(scale));
                    }

                    if (!scale && node.hasAttribute('mode')) {
                        const mode = node.getAttribute('mode');

                        if (scales.includes(scale)) {
                            scale = mode;
                        }
                    }

                    if (node.hasAttribute('limit')) {
                        limit = parseInt(node.getAttribute('limit'), 10);
                    }

                    if (node.hasAttribute('form_view_id')) {
                        formViewId = parseInt(node.getAttribute('form_view_id'), 10);
                    }

                    if (node.hasAttribute('zoom_key')) {
                        zoomKey = node.getAttribute('zoom_key');
                    }

                    if (node.hasAttribute('zoomable')) {
                        zoomable = archParseBoolean(node.getAttribute('zoomable'), zoomable);
                    }

                    if (node.hasAttribute('default_group_by')) {
                        defaultGroupBy = [];

                        const defaultGroupByAttr = node.getAttribute('default_group_by');
                        defaultGroupByAttr.split(',').forEach((attr) => {
                            defaultGroupBy.push(getGroupBy(attr, fields).fieldName);
                        });
                    }

                    if (node.hasAttribute('default_order')) {
                        defaultOrderBy = stringToOrderBy(node.getAttribute('default_order'));
                    }

                    break;
                case 'field':
                    // In timeline, we display many2many fields as tags by default
                    const widget = node.getAttribute("widget");

                    if (!widget && models[modelName][node.getAttribute('name')].type === 'many2many') {
                        node.setAttribute('widget', 'many2many_tags');
                    }

                    const fieldInfo = Field.parseFieldNode(
                        node,
                        models,
                        modelName,
                        'timeline',
                        jsClass
                    );

                    if (!node.hasAttribute('force_save')) {
                        // Force save is true by default on kanban views:
                        // this allows to write on any field regardless of its modifiers.
                        fieldInfo.forceSave = true;
                    }

                    const name = fieldInfo.name;
                    if (!(fieldInfo.name in fieldNextIds)) {
                        fieldNextIds[name] = 0;
                    }

                    const fieldId = `${fieldInfo.name}_${fieldNextIds[fieldInfo.name]++}`;
                    fieldNodes[fieldId] = fieldInfo;
                    node.setAttribute('field_id', fieldId);

                    break;
                case 'widget':
                    const widgetInfo = Widget.parseWidgetNode(node);
                    const widgetId = `widget_${++widgetNextId}`;
                    widgetNodes[widgetId] = widgetInfo;
                    node.setAttribute('widget_id', widgetId);

                    break;
                case 'img':
                    // Keep track of last update so images can be reloaded when they may have changed.
                    const attSrc = node.getAttribute('t-att-src');

                    if (
                        attSrc &&
                        /\btimeline_image\b/.test(attSrc) &&
                        !Object.values(fieldNodes).some((f) => f.name === 'write_date')
                    ) {
                        fieldNodes.write_date_0 = {name: 'write_date', type: 'datetime'};

                        if (!('write_date' in fieldNextIds)) {
                            fieldNextIds['write_date'] = 0;
                        }
                    }

                    break;
                case 'templates':
                    itemTemplate = node.querySelector('[t-name=timeline-box]') || null;

                    if (itemTemplate) {
                        itemTemplate.removeAttribute('t-name');
                    }

                    break;
            }
        });

        if (fields.display_name && !('display_name' in fieldNextIds)) {
            fieldNextIds['display_name'] = 0;
        }

        if (fields[defaultGroupBy.name] && !(defaultGroupBy.name in fieldNextIds)) {
            fieldNextIds[defaultGroupBy.name] = 0;
        }

        defaultGroupBy.forEach((field) => {
            if (!(field in fieldNextIds)) {
                fieldNextIds[field] = 0;
            }
        });

        if (zoomable) {
            scales.push('custom');
        }

        if (!scale) {
            scale = scales.includes('week') ? 'week' : scales[0];
        }

        return {
            activeActions,
            fieldNames: Object.keys(fieldNextIds),
            fieldNodes,
            widgetNodes,
            formViewId, //TODO
            scale,
            scales,
            zoomKey,
            zoomable,
            limit,
            fieldDateStart,
            fieldDateEnd,
            defaultGroupBy,
            defaultOrderBy,
            itemTemplate,
        };
    }
}
