/** @odoo-module **/

import {App, Component, onMounted, onWillStart, onWillUnmount, onWillDestroy, useEffect, useRef} from '@odoo/owl';
import {templates} from '@web/core/assets';
import {useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';
import {formatFloatTime} from '@web/views/fields/formatters';
import {useViewCompiler} from '@web/views/view_compiler';
import {TimelineCompiler} from './timeline_compiler';
import {TimelineRecord} from './timeline_record';
import {AVAILABLE_SCALES, SCALES} from './timeline_controller';

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
        'div': ['class', 'style'],
        'p': ['class', 'style'],
        'span': ['class', 'style'],
        'img': ['class', 'style', 'src', 'title', 'alt', 'width', 'height'],
    },
};

export class TimelineRenderer extends Component {
    static template = 'pyper_timeline.TimelineRenderer';

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
        createRecord: {
            //TODO props.createRecord
            type: Function,
            optional: true,
        },
        editRecord: {
            //TODO props.editRecord
            type: Function,
            optional: true,
        },
        deleteRecord: {
            //TODO props.deleteRecord
            type: Function,
            optional: true,
        },
        openRecords: {
            //TODO props.openRecords
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

        this.redraw = debounce(this.redraw, 0, false);

        const {groupTemplates, itemTemplate} = this.props.model.archInfo;
        const mapGroupTemplates = {};

        Object.keys(groupTemplates).forEach(groupName => {
            mapGroupTemplates['groupTemplate_' + groupName] = groupTemplates[groupName];
        });

        this.timelineTemplates = useViewCompiler(TimelineCompiler, {
            ...mapGroupTemplates,
            itemTemplate,
        });

        onWillStart(async () => {
            await this.pyperSetupService.register(this.constructor.SETUP_PREFIX, this.constructor.defaultSettings);
        });

        onMounted(() => {
            this.timeline = new vis.Timeline(this.timelineRef.el, [], [], this.timelineOptions);
            this.timeline.on('changed', this.onTimelineChanged.bind(this));
            this.timeline.on('rangechanged', this.onTimelineRangeChanged.bind(this));
        });

        onWillUnmount(() => {
            this.resetRendererRecords();
            this.timeline.off('changed', this.onTimelineChanged.bind(this));
            this.timeline.off('rangechanged', this.onTimelineRangeChanged.bind(this));
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
    }

    get settings() {
        return this.pyperSetupService.settings[this.constructor.SETUP_PREFIX];
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
                remove: this.props.model.canDelete,
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
            onAdd: undefined, //TODO
            onAddGroup: undefined, //TODO
            onDropObjectOnItem: undefined, //TODO
            onInitialDrawComplete: undefined, //TODO
            onMove: undefined, //TODO
            onMoveGroup: undefined, //TODO
            onMoving: undefined, //TODO
            onRemove: undefined, //TODO
            onRemoveGroup: undefined, //TODO
            onUpdate: undefined, //TODO
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
                template: undefined,
            },
            tooltipOnItemUpdateTime: {
                template: undefined,
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

    renderTemplateGroup(group, element) {
        let tplName = undefined;

        if (this.props.model.groupBy.length > 0) {
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
        // Render clustered items
        if (item.uiItems) {
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
    }

    async onTimelineRangeChanged(range) {
        if (range.byUser && this.props.setRange) {
            await this.props.setRange(DateTime.fromJSDate(range.start), DateTime.fromJSDate(range.end));
        }
    }

    async onTimelineChanged() {
        return await this.renderRecords();
    }

    onItemsChange() {
        this.resetRendererRecords();
        this.timeline.setData({
            groups: new vis.DataSet(this.props.model.groups),
            items: new vis.DataSet(this.props.model.items),
        });
    }
}
