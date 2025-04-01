/** @odoo-module **/

import {browser} from '@web/core/browser/browser';
import {visitXML} from '@web/core/utils/xml';
import {getGroupBy} from '@web/search/utils/group_by';
import {stringToOrderBy} from '@web/search/utils/order_by';
import {Field} from '@web/views/fields/field';
import {archParseBoolean, getActiveActions} from '@web/views/utils';
import {Widget} from '@web/views/widgets/widget';
import {AVAILABLE_SCALES} from './timeline_controller';

function replaceTag(el, newTagName) {
    const newEl = document.createElement(newTagName);
    [...el.children].forEach(o => newEl.appendChild(o));
    [...el.attributes].forEach(o => newEl.attributes.setNamedItem(o.cloneNode()));
    el.parentNode.replaceChild(newEl, el);

    return newEl;
}

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
        let limit = null;
        let fieldDateStart = null;
        let fieldDateEnd = null;
        let fieldColor = null;
        let fieldHtmlColor = null;
        let fieldHtmlColorOpacity = 0.4;
        let defaultGroupBy = [];
        let defaultOrderBy = null;
        let groupOrderBy = {};
        let groupByAllRecords = false;
        let useTimelineDelete = false;
        let forceEmptyGroup = false;
        let dialogSize = 'fs';
        const groupFieldNextIds = {};
        let groupTemplates = {};
        let itemTemplate = null;
        let createItemTemplate = null;
        let createItemDefaultDurationMinutes = 60;
        let createItemOnSingleClick = false;
        let popoverTemplate = undefined;
        let tooltipTemplate = undefined;
        let tooltipUpdateTemplate = undefined;
        let templateRendererModes = {};
        let hideUnworkedTimes = false;
        let itemPointType = 'box';
        let itemRangeType = 'range';
        let align = 'auto';
        let autoResize = true;
        let clickToUse = false;
        let groupHeightMode = 'auto';
        let itemsAlwaysDraggableItem = false;
        let itemsAlwaysDraggableRange = false;
        let itemOverflowVisible = false;
        let longSelectPressTime = undefined;
        let marginAxis = 4;
        let marginItemHorizontal = 0;
        let marginItemVertical = 0;
        let max = undefined;
        let maxMinorChars = 7;
        let min = undefined;
        let moveable = true;
        let multiselect = false;
        let multiselectPerGroup = false;
        let orientationAxis = 'top';
        let orientationItem = 'top';
        let preferZoom = false;
        let rollingModeFollow = false;
        let rollingModeOffset = 0.5;
        let rtl = false;
        let selectable = undefined;
        let sequentialSelection = false;
        let showCurrentTime = true;
        let showMajorLabels = true;
        let showMinorLabels = true;
        let showWeekScale = true;
        let showTooltips = true;
        let defaultStack = false;
        let stack = undefined;
        let stackSubgroups = true;
        let cluster = false;
        let clusterMaxItems = -1;
        let clusterTitleTemplate = undefined;
        let clusterShowStipes = false;
        let clusterFitOnDoubleClick = false;
        let timeAxisScale = undefined;
        let timeAxisStep = 1;
        let type = undefined;
        let tooltipFollowMouse = false;
        let tooltipOverflowMethod = 'flip';
        let tooltipDelay = 500;
        let tooltipOnItemUpdateTime = false;
        let xssDisabled = false;
        let xssFilterOptions = undefined;
        let width = '100%';
        let height = '100%';
        let minHeight = undefined;
        let maxHeight = undefined;
        let horizontalScroll = false;
        let verticalScroll = true;
        let zoomable = true;
        let zoomFriction = 40;
        let zoomKey = 'ctrlKey';
        let editableTime = true;

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
                    fieldColor = node.getAttribute('field_color');
                    fieldHtmlColor = node.getAttribute('field_html_color');
                    fieldHtmlColorOpacity = node.getAttribute('field_html_color_opacity');
                    jsClass = node.getAttribute('js_class');

                    if (node.hasAttribute('scales')) {
                        const scalesAttr = node.getAttribute('scales');
                        scales = scalesAttr.split(',').filter((scale) => AVAILABLE_SCALES.includes(scale));
                    }

                    if (!scale && node.hasAttribute('mode')) {
                        const mode = node.getAttribute('mode');

                        if (scales.includes(mode)) {
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

                    if (node.hasAttribute('editable_time')) {
                        editableTime = archParseBoolean(node.getAttribute('editable_time'), editableTime);
                    }

                    if (node.hasAttribute('zoomable')) {
                        zoomable = archParseBoolean(node.getAttribute('zoomable'), zoomable);
                    }

                    if (node.hasAttribute('group_by_all_records')) {
                        groupByAllRecords = archParseBoolean(node.getAttribute('group_by_all_records'), groupByAllRecords);
                    }

                    // Create item default duration
                    if (node.hasAttribute('default_duration')) {
                        const defaultDurationVal = parseInt(node.getAttribute('default_duration'), 10);
                        createItemDefaultDurationMinutes = defaultDurationVal || createItemDefaultDurationMinutes;
                    }

                    // Create item on single click
                    if (node.hasAttribute('create_single_click')) {
                        createItemOnSingleClick = archParseBoolean(node.getAttribute('create_single_click'), createItemOnSingleClick);
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

                    if (node.hasAttribute('use_timeline_delete')) {
                        useTimelineDelete = archParseBoolean(node.getAttribute('use_timeline_delete'), useTimelineDelete);
                    }

                    if (node.hasAttribute('force_empty_group')) {
                        forceEmptyGroup = archParseBoolean(node.getAttribute('force_empty_group'), forceEmptyGroup);
                    }

                    if (node.hasAttribute('dialog_size')) {
                        dialogSize = archParseBoolean(node.getAttribute('dialog_size'), dialogSize);
                    }

                    if (node.hasAttribute('hide_unworked_times')) {
                        hideUnworkedTimes = archParseBoolean(node.getAttribute('hide_unworked_times'), hideUnworkedTimes);
                    }

                    if (node.hasAttribute('item_point_type')) {
                        itemPointType = node.getAttribute('item_point_type');
                    }

                    if (node.hasAttribute('item_range_type')) {
                        itemRangeType = node.getAttribute('item_range_type');
                    }

                    align = node.getAttribute('align') || align;

                    if (node.hasAttribute('auto_resize')) {
                        autoResize = archParseBoolean(node.getAttribute('auto_resize'), autoResize);
                    }

                    if (node.hasAttribute('click_to_use')) {
                        clickToUse = archParseBoolean(node.getAttribute('click_to_use'), clickToUse);
                    }

                    if (node.hasAttribute('group_height_mode')) {
                        groupHeightMode = archParseBoolean(node.getAttribute('group_height_mode'), groupHeightMode);
                    }

                    if (node.hasAttribute('items_always_draggable_item')) {
                        itemsAlwaysDraggableItem = archParseBoolean(node.getAttribute('items_always_draggable_item'), itemsAlwaysDraggableItem);
                    }

                    if (node.hasAttribute('items_always_draggable_range')) {
                        itemsAlwaysDraggableRange = archParseBoolean(node.getAttribute('items_always_draggable_range'), itemsAlwaysDraggableRange);
                    }

                    if (node.hasAttribute('item_overflow_visible')) {
                        itemOverflowVisible = archParseBoolean(node.getAttribute('item_overflow_visible'), itemOverflowVisible);
                    }

                    if (node.hasAttribute('long_select_press_time')) {
                        longSelectPressTime = parseInt(node.getAttribute('long_select_press_time'), 10);
                    }

                    if (node.hasAttribute('margin_axis')) {
                        marginAxis = parseInt(node.getAttribute('margin_axis'), 10);
                    }

                    if (node.hasAttribute('margin_item_horizontal')) {
                        marginItemHorizontal = parseInt(node.getAttribute('margin_item_horizontal'), 10);
                    }

                    if (node.hasAttribute('margin_item_vertical')) {
                        marginItemVertical = parseInt(node.getAttribute('margin_item_vertical'), 10);
                    }

                    if (node.hasAttribute('max')) {
                        max = node.getAttribute('max');
                    }

                    if (node.hasAttribute('max_minor_chars')) {
                        maxMinorChars = parseInt(node.getAttribute('max_minor_chars'), 10);
                    }

                    if (node.hasAttribute('min')) {
                        min = node.getAttribute('min');
                    }

                    if (node.hasAttribute('moveable')) {
                        moveable = archParseBoolean(node.getAttribute('moveable'), moveable);
                    }

                    if (node.hasAttribute('multiselect')) {
                        multiselect = archParseBoolean(node.getAttribute('multiselect'), multiselect);
                    }

                    if (node.hasAttribute('multiselect_per_group')) {
                        multiselectPerGroup = archParseBoolean(node.getAttribute('multiselect_per_group'), multiselectPerGroup);
                    }

                    if (node.hasAttribute('orientation_axis')) {
                        orientationAxis = node.getAttribute('orientation_axis');
                    }

                    if (node.hasAttribute('orientation_item')) {
                        orientationItem = node.getAttribute('orientation_item');
                    }

                    if (node.hasAttribute('prefer_zoom')) {
                        preferZoom = archParseBoolean(node.getAttribute('prefer_zoom'), preferZoom);
                    }

                    if (node.hasAttribute('rolling_mode_follow')) {
                        rollingModeFollow = archParseBoolean(node.getAttribute('rolling_mode_follow'), rollingModeFollow);
                    }

                    if (node.hasAttribute('rolling_mode_offset')) {
                        rollingModeOffset = parseFloat(node.getAttribute('rolling_mode_offset'));
                    }

                    if (node.hasAttribute('rtl')) {
                        rtl = archParseBoolean(node.getAttribute('rtl'), rtl);
                    }

                    if (node.hasAttribute('selectable')) {
                        selectable = archParseBoolean(node.getAttribute('selectable'), selectable);
                    }

                    if (node.hasAttribute('sequential_selection')) {
                        sequentialSelection = archParseBoolean(node.getAttribute('sequential_selection'), sequentialSelection);
                    }

                    if (node.hasAttribute('show_current_time')) {
                        showCurrentTime = archParseBoolean(node.getAttribute('show_current_time'), showCurrentTime);
                    }

                    if (node.hasAttribute('show_major_labels')) {
                        showMajorLabels = archParseBoolean(node.getAttribute('show_major_labels'), showMajorLabels);
                    }

                    if (node.hasAttribute('show_minor_labels')) {
                        showMinorLabels = archParseBoolean(node.getAttribute('show_minor_labels'), showMinorLabels);
                    }

                    if (node.hasAttribute('show_week_scale')) {
                        showWeekScale = archParseBoolean(node.getAttribute('show_week_scale'), showWeekScale);
                    }

                    if (node.hasAttribute('show_tooltips')) {
                        showTooltips = archParseBoolean(node.getAttribute('show_tooltips'), showTooltips);
                    }

                    if (node.hasAttribute('default_stack')) {
                        defaultStack = archParseBoolean(node.getAttribute('default_stack'), defaultStack);
                    }

                    if (node.hasAttribute('stack')) {
                        stack = archParseBoolean(node.getAttribute('stack'), stack);
                    }

                    if (node.hasAttribute('stack_subgroups')) {
                        stackSubgroups = archParseBoolean(node.getAttribute('stack_subgroups'), stackSubgroups);
                    }

                    if (node.hasAttribute('cluster')) {
                        cluster = archParseBoolean(node.getAttribute('cluster'), stackSubgroups);
                    }

                    if (node.hasAttribute('cluster_max_items')) {
                        clusterMaxItems = parseInt(node.getAttribute('cluster_max_items'), 10);
                    }

                    if (node.hasAttribute('cluster_title_template')) {
                        clusterTitleTemplate = node.getAttribute('cluster_title_template');
                    }

                    if (node.hasAttribute('cluster_show_stipes')) {
                        clusterShowStipes = archParseBoolean(node.getAttribute('cluster_show_stipes'), clusterShowStipes);
                    }

                    if (node.hasAttribute('cluster_fit_on_double_click')) {
                        clusterFitOnDoubleClick = archParseBoolean(node.getAttribute('cluster_fit_on_double_click'), clusterFitOnDoubleClick);
                    }

                    if (node.hasAttribute('time_axis_scale')) {
                        timeAxisScale = node.getAttribute('time_axis_scale');
                    }

                    if (node.hasAttribute('time_axis_step')) {
                        timeAxisStep = parseInt(node.getAttribute('time_axis_step'), 10);
                    }

                    if (node.hasAttribute('type')) {
                        type = node.getAttribute('type');
                    }

                    if (node.hasAttribute('tooltip_follow_mouse')) {
                        tooltipFollowMouse = archParseBoolean(node.getAttribute('tooltip_follow_mouse'), tooltipFollowMouse);
                    }

                    if (node.hasAttribute('tooltip_overflow_method')) {
                        tooltipOverflowMethod = node.getAttribute('tooltip_overflow_method');
                    }

                    if (node.hasAttribute('tooltip_delay')) {
                        tooltipDelay = parseInt(node.getAttribute('tooltip_delay'), 10);
                    }

                    if (node.hasAttribute('tooltip_on_item_update_time')) {
                        tooltipOnItemUpdateTime = archParseBoolean(node.getAttribute('tooltip_on_item_update_time'), tooltipOnItemUpdateTime);
                    }

                    if (node.hasAttribute('xss_disabled')) {
                        xssDisabled = archParseBoolean(node.getAttribute('xss_disabled'), xssDisabled);
                    }

                    if (node.hasAttribute('xss_filter_options')) {
                        xssFilterOptions = JSON.parse(node.getAttribute('xss_filter_options'));
                    }

                    if (node.hasAttribute('width')) {
                        width = node.getAttribute('width');
                    }

                    if (node.hasAttribute('height')) {
                        height = node.getAttribute('height');
                    }

                    if (node.hasAttribute('min_height')) {
                        minHeight = node.getAttribute('min_height');
                    }

                    if (node.hasAttribute('max_height')) {
                        maxHeight = node.getAttribute('max_height');
                    }

                    if (node.hasAttribute('horizontal_scroll')) {
                        horizontalScroll = archParseBoolean(node.getAttribute('horizontal_scroll'), horizontalScroll);
                    }

                    if (node.hasAttribute('vertical_scroll')) {
                        verticalScroll = archParseBoolean(node.getAttribute('vertical_scroll'), verticalScroll);
                    }

                    if (node.hasAttribute('zoom_friction')) {
                        zoomFriction = parseInt(node.getAttribute('zoom_friction'), 10);
                    }

                    break;
                case 'field':
                case 'group-field':
                    // In timeline, we display many2many fields as tags by default
                    const widget = node.getAttribute('widget');
                    let groupTag = false;

                    // Restore the field tag (group-field is used because view xml convert validates fields of root model)
                    if (node.tagName === 'group-field') {
                        groupTag = true;
                        node = replaceTag(node, 'field');
                    }

                    if (!widget && fields[node.getAttribute('name')]?.type === 'many2many') {
                        node.setAttribute('widget', 'many2many_tags');
                    }

                    const parentGroup = node.closest('[t-name=timeline-group]');
                    const fieldForGroup = !!parentGroup || groupTag;

                    if (fieldForGroup) {
                        // Group Field
                        let fieldGroupBy = parentGroup?.getAttribute('group_by');

                        if (!fieldGroupBy && groupTag) {
                            fieldGroupBy = node.getAttribute('group_by');
                        }

                        if (!fieldGroupBy && groupTag) {
                            throw new TimelineParseArchError('The "group_by" attribute on "group-field" tag is ' +
                                'required when "group-field" tag is not child of the Timeline ' +
                                'template "timeline-group"');
                        }

                        fieldGroupBy = fieldGroupBy || 'default';
                        const groupFieldInfo = {
                            name: node.getAttribute('name'),
                            type: undefined,
                            viewType: 'timeline',
                            widget: node.getAttribute('widget'),
                            field: undefined,
                            context: '{}',
                            string: undefined,
                            help: undefined,
                            onChange: false,
                            forceSave: false,
                            options: {},
                            decorations: {},
                            attrs: {},
                            domain: undefined,
                        }
                        const name = groupFieldInfo.name;

                        // Init group categories
                        if (!groupFieldNextIds[fieldGroupBy]) {
                            groupFieldNextIds[fieldGroupBy] = {};
                        }

                        // Configure node
                        if (!(groupFieldInfo.name in groupFieldNextIds[fieldGroupBy])) {
                            groupFieldNextIds[fieldGroupBy][name] = 0;
                        }

                        const groupFieldId = `${groupFieldInfo.name}_${groupFieldNextIds[fieldGroupBy][groupFieldInfo.name]++}`;
                        node.setAttribute('field_id', groupFieldId);
                    } else {
                        // Item Field
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
                    }

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
                    // Group templates
                    const queryGroupTemplates = node.querySelectorAll('[t-name=timeline-group]') || [];

                    if (queryGroupTemplates.length > 0) {
                        queryGroupTemplates.forEach((gtEl) => {
                            const groupByName = gtEl.getAttribute('group_by') || 'default';
                            const groupByOrder = gtEl.getAttribute('order') || undefined;

                            if (groupTemplates[groupByName]) {
                                throw new TimelineParseArchError(
                                    `Timeline group for the grouped field "${groupByName}" must be defined only one time`
                                );
                            }

                            groupTemplates[groupByName] = gtEl;
                            templateRendererModes['groupTemplate_' + groupByName] = gtEl.getAttribute('renderer_mode') || 'static';

                            if (groupByName !== 'default' && groupByOrder) {
                                groupOrderBy[groupByName] = stringToOrderBy(groupByOrder);
                            }
                        });
                    }

                    // Item template
                    itemTemplate = node.querySelector('[t-name=timeline-item]') || null;

                    if (itemTemplate) {
                        itemTemplate.removeAttribute('t-name');
                        templateRendererModes['itemTemplate'] = itemTemplate.getAttribute('renderer_mode') || 'static';
                    }

                    // Create item template
                    createItemTemplate = node.querySelector('[t-name=timeline-item-create]') || null;

                    if (createItemTemplate) {
                        createItemTemplate.removeAttribute('t-name');
                        templateRendererModes['createItemTemplate'] = createItemTemplate.getAttribute('renderer_mode') || 'static';
                    }

                    // Popover template
                    popoverTemplate = node.querySelector('[t-name=timeline-popover]') || null;

                    if (popoverTemplate) {
                        popoverTemplate.removeAttribute('t-name');
                    }

                    // Tooltip template
                    tooltipTemplate = node.querySelector('[t-name=timeline-tooltip]') || null;

                    if (tooltipTemplate) {
                        tooltipTemplate.removeAttribute('t-name');
                    }

                    // Tooltip update template
                    tooltipUpdateTemplate = node.querySelector('[t-name=timeline-tooltip-update]') || null;

                    if (tooltipUpdateTemplate) {
                        tooltipUpdateTemplate.removeAttribute('t-name');
                    }

                    break;
            }
        });

        if (fields[fieldDateStart] && !(fieldDateStart in fieldNextIds)) {
            fieldNextIds[fieldDateStart] = 0;
        }

        if (fields[fieldDateEnd] && !(fieldDateEnd in fieldNextIds)) {
            fieldNextIds[fieldDateEnd] = 0;
        }

        if (fields[fieldHtmlColor] && !(fieldHtmlColor in fieldNextIds)) {
            fieldNextIds[fieldHtmlColor] = 0;
        }

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

        const groupFieldNames = {};

        Object.keys(groupFieldNextIds).forEach(groupField => {
            groupFieldNames[groupField] = [...Object.keys(groupFieldNextIds[groupField])]
        });

        return {
            activeActions,
            fieldNames: [...Object.keys(fieldNextIds)],
            fieldNodes,
            widgetNodes,
            formViewId,
            scale,
            scales,
            limit,
            fieldDateStart,
            fieldDateEnd,
            fieldColor,
            fieldHtmlColor,
            fieldHtmlColorOpacity,
            defaultGroupBy,
            defaultOrderBy,
            groupOrderBy,
            groupByAllRecords,
            useTimelineDelete,
            forceEmptyGroup,
            dialogSize,
            groupFieldNames,
            groupTemplates,
            itemTemplate,
            createItemTemplate,
            createItemDefaultDurationMinutes,
            createItemOnSingleClick,
            popoverTemplate,
            tooltipTemplate,
            tooltipUpdateTemplate,
            templateRendererModes,
            hideUnworkedTimes,
            itemPointType,
            itemRangeType,
            align,
            autoResize,
            clickToUse,
            groupHeightMode,
            itemsAlwaysDraggableItem,
            itemsAlwaysDraggableRange,
            itemOverflowVisible,
            longSelectPressTime,
            marginAxis,
            marginItemHorizontal,
            marginItemVertical,
            max,
            maxMinorChars,
            min,
            moveable,
            multiselect,
            multiselectPerGroup,
            orientationAxis,
            orientationItem,
            preferZoom,
            rollingModeFollow,
            rollingModeOffset,
            rtl,
            selectable,
            sequentialSelection,
            showCurrentTime,
            showMajorLabels,
            showMinorLabels,
            showWeekScale,
            showTooltips,
            defaultStack,
            stack,
            stackSubgroups,
            cluster,
            clusterMaxItems,
            clusterTitleTemplate,
            clusterShowStipes,
            clusterFitOnDoubleClick,
            timeAxisScale,
            timeAxisStep,
            type,
            tooltipFollowMouse,
            tooltipOverflowMethod,
            tooltipDelay,
            tooltipOnItemUpdateTime,
            xssDisabled,
            xssFilterOptions,
            width,
            height,
            minHeight,
            maxHeight,
            horizontalScroll,
            verticalScroll,
            zoomable,
            zoomFriction,
            zoomKey,
            editableTime,
        };
    }
}
