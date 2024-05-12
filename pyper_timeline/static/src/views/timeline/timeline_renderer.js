/** @odoo-module **/

import {
    App,
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    onWillDestroy,
    useEffect,
    useRef,
    useState,
} from '@odoo/owl';
import {templates} from '@web/core/assets';
import {formatDateTime, serializeDateTime} from '@web/core/l10n/dates';
import {localization} from '@web/core/l10n/localization';
import {_t} from '@web/core/l10n/translation';
import {usePopover} from '@web/core/popover/popover_hook';
import {useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';
import {renderToElement, renderToString} from '@web/core/utils/render';
import {formatFloatTime} from '@web/views/fields/formatters';
import {useViewCompiler} from '@web/views/view_compiler';
import {TimelineCompiler} from './timeline_compiler';
import {TimelinePopover} from './timeline_popover';
import {TimelineRecord} from './timeline_record';
import {AVAILABLE_SCALES, SCALES} from './timeline_controller';
import {UNASSIGNED_ID} from './timeline_model';

const {DateTime} = luxon;

function removeNestedUndefined(obj) {
    for (const key in obj) {
        if (obj[key] === undefined) {
            delete obj[key];
        } else if (typeof obj[key] === 'object') {
            removeNestedUndefined(obj[key]);
        }
    }

    return obj;
}

function deepMerge(obj1, obj2) {
    const result = {...obj1};

    for (let key in obj2) {
        if (obj2.hasOwnProperty(key)) {
            if (obj2[key] instanceof Object && obj1[key] instanceof Object) {
                result[key] = deepMerge(obj1[key], obj2[key]);
            } else {
                result[key] = obj2[key];
            }
        }
    }

    return result;
}

export const DEFAULT_XSS_FILTER_OPTIONS = {
    'allowList': {
        'strong': true,
        'i': true,
        'b': true,
        'br': true,
        'div': ['class', 'style'],
        'p': ['class', 'style'],
        'span': ['class', 'style'],
        'img': ['class', 'style', 'src', 'title', 'alt', 'width', 'height'],
    },
};

export class TimelineRenderer extends Component {
    static template = 'pyper_timeline.TimelineRenderer';

    static components = {
        Popover: TimelinePopover,
    };

    static props = {
        model: {
            type: Object,
            optional: true,
        },
        isWeekendVisible: {
            type: Boolean,
            optional: true,
        },
        setRange: {
            type: Function,
            optional: true,
        },
        editRecord: {
            type: Function,
            optional: true,
        },
        deleteRecord: {
            type: Function,
            optional: true,
        },
        openDialog: {
            type: Function,
            optional: true,
        },
        openRecords: {
            type: Function,
            optional: true,
        },
    };

    static defaultSettings = {
        visibleTimeRangeStart: false,
        visibleTimeRangeEnd: false,
    };

    static SETUP_PREFIX = 'pyper_timeline.timeline.';

    setup() {
        this.pyperSetupService = useService('pyper_setup');
        this.uiService = useService('ui');
        this.notificationService = useService('notification');
        this.timelineRef = useRef('timeline');
        this.timeline = null;
        this.rendererRecords = new Map();
        this.toRendererRecords = new Map();
        this.state = useState({
            loading: true,
            saving : false,
        });

        this.redraw = debounce(this.redraw, 0, false);

        this.popover = usePopover(this.constructor.components.Popover, this.popoverOptions);

        const {
            groupTemplates,
            itemTemplate,
            popoverTemplate,
            tooltipTemplate,
            tooltipUpdateTemplate,
        } = this.props.model.archInfo;
        const templates = {};

        Object.keys(groupTemplates).forEach(groupName => {
            templates['groupTemplate_' + groupName] = groupTemplates[groupName];
        });

        if (itemTemplate) {
            templates['itemTemplate'] = itemTemplate;
        }

        if (popoverTemplate) {
            templates['popoverTemplate'] = popoverTemplate;
        }

        if (tooltipTemplate) {
            templates['tooltipTemplate'] = tooltipTemplate;
        }

        if (tooltipUpdateTemplate) {
            templates['tooltipUpdateTemplate'] = tooltipUpdateTemplate;
        }

        this.timelineTemplates = useViewCompiler(TimelineCompiler, templates);

        onWillStart(async () => {
            await this.pyperSetupService.register(this.constructor.SETUP_PREFIX, this.constructor.defaultSettings);
        });

        onMounted(() => {
            this.timeline = new vis.Timeline(this.timelineRef.el, [], [], this.timelineOptions);
            this.timeline.on('changed', this.onTimelineChanged.bind(this));
            this.timeline.on('rangechange', this.onTimelineRangeChange.bind(this));
            this.timeline.on('rangechanged', this.onTimelineRangeChanged.bind(this));
            this.timeline.on('click', this.onClick.bind(this));
            this.timeline.on('doubleClick', this.doubleClick.bind(this));
        });

        onWillUnmount(() => {
            this.resetRendererRecords();
            this.timeline.off('changed', this.onTimelineChanged.bind(this));
            this.timeline.off('rangechange', this.onTimelineRangeChange.bind(this));
            this.timeline.off('rangechanged', this.onTimelineRangeChanged.bind(this));
            this.timeline.off('click', this.onClick.bind(this));
            this.timeline.off('doubleClick', this.doubleClick.bind(this));
            this.timeline.destroy();
            this.timeline = null;
        });

        onWillDestroy(() => {
            this.pyperSetupService.unregister(this.constructor.SETUP_PREFIX);
        });

        useEffect(() => {
            this.timeline.setOptions(this.timelineOptions);
        }, () => [this.timelineOptions]);

        useEffect(() => {
            this.timeline.setWindow(
                this.props.model.rangeStart.toJSDate(),
                this.props.model.rangeEnd.toJSDate(),
                {animation: false},
            );
        }, () => [this.props.model.rangeStart, this.props.model.rangeEnd]);

        useEffect(() => {
            this.onItemsChange();
        }, () => [this.props.model.groups, this.props.model.items]);

        useEffect(() => {
            if (this.props.model.loading) {
                this.state.loading = true;
            }
        }, () => [this.props.model.loading]);
    }

    get settings() {
        return this.pyperSetupService.settings[this.constructor.SETUP_PREFIX];
    }

    get timelineClasses() {
        return {
            'timeline-loading': this.state.loading,
            'overflow-visibility': this.props.model.archInfo.itemOverflowVisible,
        }
    }

    get visibleTimeRangeStart() {
        return formatFloatTime(this.settings.visibleTimeRangeStart, {displaySeconds: true}) || undefined;
    }

    get visibleTimeRangeEnd() {
        return formatFloatTime(this.settings.visibleTimeRangeEnd, {displaySeconds: true}) || undefined;
    }

    get timelineSelectable() {
        return this.props.model.archInfo.selectable
            || this.props.model.canCreate
            || this.props.model.canEdit
            || this.props.model.canRemove
        ;
    }

    get timelineOptions() {
        const hiddenDates = [];

        if (this.visibleTimeRangeStart) {
            hiddenDates.push({
                start: '0000-01-01 00:00:00',
                end: '0000-01-01 ' + this.visibleTimeRangeStart,
                repeat: 'daily',
            });
        }

        if (this.visibleTimeRangeEnd) {
            hiddenDates.push({
                start: '0000-01-01 ' + this.visibleTimeRangeEnd,
                end: '0000-01-02 00:00:00',
                repeat: 'daily',
            });
        }

        if (!this.props.isWeekendVisible && this.props.model.weekends.length === 2) {
            hiddenDates.push({
                start: this.props.model.weekends[0].toJSDate(),
                end: this.props.model.weekends[1].plus({days: 1}).toJSDate(),
                repeat: 'weekly',
            });
        }

        const availableScales = AVAILABLE_SCALES.filter(s => this.props.model.archInfo.scales.includes(s));
        let zoomMin = SCALES[availableScales[0] || 'day']?.zoom || undefined;
        let zoomMax = SCALES[availableScales[availableScales.length - 1] || 'year']?.zoom || undefined;

        // All options with undefined values and so without arch parser values indicates that the options are not
        // useful for Owl integration. On the other hand and if necessary, it is always possible to use a "js_class"
        // and override the Timeline options.
        return removeNestedUndefined({
            align: this.props.model.archInfo.align,
            autoResize: this.props.model.archInfo.autoResize,
            clickToUse: this.props.model.archInfo.clickToUse,
            configure: false,
            dataAttributes: [],
            editable: {
                add: this.props.model.canCreate,
                remove: this.props.model.canDelete && this.props.model.archInfo.useTimelineDelete,
                updateGroup: this.props.model.canEdit,
                updateTime: this.props.model.canEdit,
                overrideItems: this.props.model.canEdit,
            },
            format: undefined,
            groupEditable: {
                add: false,
                remove: false,
                order: false,
            },
            groupHeightMode: this.props.model.archInfo.groupHeightMode,
            groupOrder: undefined,
            groupOrderSwap: undefined,
            groupTemplate: this.renderTemplateGroup.bind(this),
            hiddenDates,
            itemsAlwaysDraggable: {
                item: this.props.model.archInfo.itemsAlwaysDraggableItem,
                range: this.props.model.archInfo.itemsAlwaysDraggableRange,
            },
            locale: undefined,
            locales: undefined,
            longSelectPressTime: this.props.model.archInfo.longSelectPressTime,
            moment: vis.moment,
            margin: {
                axis: this.props.model.archInfo.marginAxis,
                item: {
                    horizontal: this.props.model.archInfo.marginItemHorizontal,
                    vertical: this.props.model.archInfo.marginItemVertical,
                },
            },
            max: this.props.model.archInfo.max,
            maxMinorChars: this.props.model.archInfo.maxMinorChars,
            min: this.props.model.archInfo.min,
            moveable: this.props.model.archInfo.moveable,
            multiselect: this.props.model.archInfo.multiselect,
            multiselectPerGroup: this.props.model.archInfo.multiselectPerGroup,
            onAdd: this.onTimelineAdd.bind(this),
            onAddGroup: undefined,
            onDropObjectOnItem: undefined,
            onInitialDrawComplete: undefined,
            onMove: this.onTimelineMove.bind(this),
            onMoveGroup: undefined,
            onMoving: this.onTimelineMoving.bind(this),
            onRemove: this.onTimelineRemove.bind(this),
            onRemoveGroup: undefined,
            order: undefined, // Custom ordering is not suitable for large amounts of items.
            orientation: {
                axis: this.props.model.archInfo.orientationAxis,
                item: this.props.model.archInfo.orientationItem,
            },
            preferZoom: this.props.model.archInfo.preferZoom,
            rollingMode: {
                follow: this.props.model.archInfo.rollingModeFollow,
                offset: this.props.model.archInfo.rollingModeOffset,
            },
            rtl: this.props.model.archInfo.rtl,
            selectable: this.timelineSelectable,
            sequentialSelection: this.props.model.archInfo.sequentialSelection,
            showCurrentTime: this.props.model.archInfo.showCurrentTime,
            showMajorLabels: this.props.model.archInfo.showMajorLabels,
            showMinorLabels: this.props.model.archInfo.showMinorLabels,
            showWeekScale: this.props.model.archInfo.showWeekScale,
            showTooltips: this.props.model.archInfo.showTooltips,
            stack: this.props.model.archInfo.stack,
            stackSubgroups: this.props.model.archInfo.stackSubgroups,
            cluster: {
                maxItems: this.props.model.archInfo.clusterMaxItems,
                titleTemplate: this.props.model.archInfo.clusterTitleTemplate,
                clusterCriteria: (/* firstItem, secondItem */) => {
                    return SCALES[this.props.model.scale]?.clustering || false;
                },
                showStipes: this.props.model.archInfo.clusterShowStipes,
                fitOnDoubleClick: this.props.model.archInfo.clusterFitOnDoubleClick,
            },
            snap: undefined,
            template: this.renderTemplateItem.bind(this),
            loadingScreenTemplate: undefined,
            visibleFrameTemplate: undefined,
            timeAxis: {
                scale: this.props.model.archInfo.timeAxisScale,
                step: this.props.model.archInfo.timeAxisStep,
            },
            type: this.props.model.archInfo.type,
            tooltip: {
                followMouse: this.props.model.archInfo.tooltipFollowMouse,
                overflowMethod: this.props.model.archInfo.tooltipOverflowMethod,
                delay: this.props.model.archInfo.tooltipDelay,
                template: this.renderTemplateTooltip.bind(this),
            },
            tooltipOnItemUpdateTime: !this.props.model.archInfo.tooltipOnItemUpdateTime ? false : {
                template: this.renderTemplateTooltipOnItemUpdateTime.bind(this),
            },
            xss: {
                disabled: this.props.model.archInfo.xssDisabled,
                filterOptions: deepMerge(DEFAULT_XSS_FILTER_OPTIONS, this.props.model.archInfo.xssFilterOptions || {}),
            },
            width: this.props.model.archInfo.width,
            height: this.props.model.archInfo.height,
            minHeight: this.props.model.archInfo.minHeight,
            maxHeight: this.props.model.archInfo.maxHeight,
            horizontalScroll: this.props.model.archInfo.horizontalScroll,
            verticalScroll: this.props.model.archInfo.verticalScroll,
            zoomable: this.props.model.archInfo.zoomable,
            zoomFriction: this.props.model.archInfo.zoomFriction,
            zoomKey: this.props.model.archInfo.zoomKey,
            zoomMin,
            zoomMax,
            start: undefined,
            end: undefined,
        });
    }

    get popoverOptions() {
        const deleteBtn = this.props.model.archInfo.useTimelineDelete;

        return {
            position: deleteBtn || localization.direction === 'rtl' ? 'bottom' : 'right',
            animation: false,
            popoverClass: 'o_timeline_item_popover',
        };
    }

    getPopoverProps(item) {
        const {record} = item;
        const displayName = record.data.display_name;
        const {canEdit, canDelete} = this.props.model;
        const {fieldDateStart, fieldDateEnd} = this.props.model.archInfo;

        return {
            archInfo: this.props.model.archInfo,
            Compiler: TimelineCompiler,
            label: displayName,
            record,
            context: {
                name: displayName,
                start: record.data[fieldDateStart].toFormat('f'),
                end: record.data[fieldDateEnd]?.toFormat('f'),
            },
            templateName: this.timelineTemplates['popoverTemplate'] ? 'popoverTemplate' : undefined,
            templates: this.timelineTemplates,
            editButton: {
                text: canEdit ? _t('Edit') : _t('View'),
                onClick: () => {
                    this.props.model.mutex.exec(() => this.props.openDialog({resId: record.data.id}));
                },
            },
            deleteButton: canDelete ? {
                text: _t('Delete'),
                onClick: async () => {
                    await this._deleteRecord(item.id);
                },
            } : undefined,
        };
    }

    renderTemplateTooltip(item, updatedData) {
        if (this.timelineTemplates['tooltipTemplate']) {
            return renderToElement(this.timelineTemplates['tooltipTemplate'], {
                ...updatedData,
            });
        }
    }

    renderTemplateTooltipOnItemUpdateTime(item) {
        const template = this.timelineTemplates['tooltipUpdateTemplate']
            ? this.timelineTemplates['tooltipUpdateTemplate']
            : 'pyper_timeline.TimelineRenderer.TooltipUpdate';

        return renderToString(template, {
            ...item,
            formatDateTime,
            luxonStart: DateTime.fromJSDate(item.start),
            luxonEnd: item.end ? DateTime.fromJSDate(item.end) : undefined,
        });
    }

    renderTemplateGroup(group, element) {
        if (!group) {
            return '';
        }

        let tplName = undefined;

        if (group.groupByField !== false && this.props.model.groupBy.length > 0) {
            tplName = 'groupTemplate_' + this.props.model.groupBy[0];

            if (!this.timelineTemplates[tplName]) {
                tplName = undefined;
            }
        }

        if (!tplName) {
            tplName = 'groupTemplate_default';

            if (!this.timelineTemplates[tplName]) {
                tplName = undefined;
            }
        }

        if (!tplName) {
            return group.content;
        }

        this.renderTemplateRecord(group, element, tplName, true);

        // Return empty string to avoid to display the id value displayed by default
        return '';
    }

    renderTemplateItem(item, element) {
        // Render clustered items or single item without template
        if (item.uiItems || !this.timelineTemplates['itemTemplate']) {
            return item.content;
        }

        // Render single item
        const readonly = !this.props.model.canEdit;
        this.renderTemplateRecord(item, element, 'itemTemplate', readonly);
    }

    renderTemplateRecord(item, element, templateName, readonly) {
        if (!this.rendererRecords.has(element)) {
            const rendererItem = {
                item,
                mounted: false,
                app: new App(TimelineRecord, {
                    env: this.constructor.env,
                    props: {
                        archInfo: this.props.model.archInfo,
                        Compiler: TimelineCompiler,
                        readonly,
                        label: item?.content,
                        record: item?.record || {},
                        templateName,
                        templates: this.timelineTemplates,
                    },
                    templates: templates,
                }),
            };

            this.rendererRecords.set(element, rendererItem);
            this.toRendererRecords.set(element, rendererItem);
        }
    }

    resetRendererRecords() {
        this.rendererRecords.forEach((rendererItem, element) => {
            if (rendererItem.app && rendererItem.mounted) {
                rendererItem.app.destroy();
                element.innerHTML = '';
            }
        });

        this.rendererRecords.clear();
        this.toRendererRecords.clear();
    }

    async renderRecords() {
        const renderedRecords = [];
        const parallelPromises = [];

        this.toRendererRecords.forEach((rendererRecord, element) => {
            if (!rendererRecord.mounted && document.contains(element)) {
                parallelPromises.push(rendererRecord.app.mount(element).then(this.redraw.bind(this)));
                rendererRecord.mounted = true;
                renderedRecords.push(element);
            }
        });

        renderedRecords.forEach((element) => {
            this.toRendererRecords.delete(element);
        });

        return Promise.all(parallelPromises);
    }

    redraw() {
        this.timeline?.redraw();
        this.state.loading = false;
    }

    async onTimelineRangeChange(range) {
        this.state.loading = true;
    }

    async onTimelineRangeChanged(range) {
        if (range.byUser && this.props.setRange) {
            await this.props.setRange(DateTime.fromJSDate(range.start), DateTime.fromJSDate(range.end));
        }
    }

    onClick(eventProps) {
        if (this.popover.isOpen || !eventProps.item || this.state.saving) {
            return;
        }

        const item = this.timeline.itemsData.get(eventProps.item);
        const popoverTarget = eventProps.event.target.closest('.vis-item');

        this.popover.open(popoverTarget, this.getPopoverProps(item));
    }

    doubleClick(eventProps) {
        if (eventProps.what === 'item' && eventProps.item) {
            // Value of eventProps.item is Integer
            this.props.model.mutex.exec(() => this.props.openRecords([eventProps.item]));
        }
    }

    async onTimelineChanged() {
        return await this.renderRecords();
    }

    onItemsChange() {
        this.resetRendererRecords();
        this.timeline.setData({
            groups: this.props.model.groups,
            items: this.props.model.items,
        });
    }

    onTimelineAdd(item, callback) {
        const context = {};
        const ctxFieldStart = 'default_' + this.props.model.archInfo.fieldDateStart;

        context[ctxFieldStart] = serializeDateTime(DateTime.fromJSDate(item.start));

        if (item.group && this.props.model.groupBy.length > 0) {
            context['default_' + this.props.model.groupBy[0]] = item.group;
        }

        this.props.openDialog({
            context,
            onRecordSaved: async () => {
                await this.props.model.load();
            },
            onRecordDiscarded: async () => {
                callback(null);
            }
        });
    }

    async onTimelineMove(item, callback) {
        this.state.saving = true;

        if (this.popover?.isOpen) {
            this.popover.close();
        }

        const record = {
            id: item.id,
            [this.props.model.archInfo.fieldDateStart]: serializeDateTime(DateTime.fromJSDate(item.start)),
        };

        if (this.props.model.archInfo.fieldDateEnd) {
            record[this.props.model.archInfo.fieldDateEnd] = item.end ? serializeDateTime(DateTime.fromJSDate(item.end)) : false;
        }

        if (this.props.model.groupBy.length > 0) {
            record[this.props.model.groupBy[0]] = item.group === UNASSIGNED_ID ? false : item.group;
        }

        const res = await this.props.editRecord(record);
        this.state.saving = false;

        if (res) {
            await this.props.model.load();
        }

        callback(res ? item : null);
    }

    async onTimelineMoving(item, callback) {
        if (this.popover?.isOpen) {
            this.popover.close();
        }

        callback(item);
    }

    async onTimelineRemove(item, callback) {
        const res = await this._deleteRecord(item.id);
        callback(res ? item : null);
    }

    async _deleteRecord(id) {
        this.state.saving = true;
        const res = await this.props.deleteRecord(id);
        this.state.saving = false;

        if (res) {
            await this.props.model.load();
        }

        return res;
    }
}
