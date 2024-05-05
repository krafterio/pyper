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

        return removeNestedUndefined({
            align: 'auto', //TODO
            autoResize: true, //TODO
            clickToUse: false, //TODO
            configure: false, //TODO
            dataAttributes: [], //TODO
            editable: false,
            format: undefined, //TODO
            groupEditable: {
                add: false, //TODO
                remove: false, //TODO
                order: false,
            },
            groupHeightMode: 'auto', //TODO
            groupOrder: 'sequence', //TODO
            groupOrderSwap: undefined, //TODO
            groupTemplate: this.renderTemplateGroup.bind(this),
            hiddenDates,
            itemsAlwaysDraggable: {
                item: false, //TODO
                range: false, //TODO
            },
            locale: undefined, //TODO
            locales: undefined, //TODO
            longSelectPressTime: 251, //TODO
            moment: vis.moment,
            margin: {
                axis: 20, //TODO
                item: {
                    horizontal: 10, //TODO
                    vertical: 10, //TODO
                },
            },
            max: undefined, //TODO
            maxMinorChars: 7, //TODO
            min: undefined, //TODO
            moveable: true, //TODO
            multiselect: false, //TODO
            multiselectPerGroup: false, //TODO
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
                axis: 'top', //TODO
                item: 'top', //TODO
            },
            preferZoom: false, //TODO
            rollingMode: {
                follow: false, //TODO
                offset: 0.5, //TODO
            },
            rtl: false, //TODO
            selectable: false, //TODO
            sequentialSelection: false, //TODO
            showCurrentTime: true, //TODO
            showMajorLabels: true, //TODO
            showMinorLabels: true, //TODO
            showWeekScale: true, //TODO
            showTooltips: true, //TODO
            stack: false, //TODO
            stackSubgroups: true, //TODO
            cluster: {
                maxItems: -1, //TODO
                titleTemplate: undefined, //TODO
                clusterCriteria: (firstItem, secondItem) => {
                    return SCALES[this.props.model.scale]?.clustering || false;
                }, //TODO allow to use custom clusterCriteria (return undefined to use default value)
                showStipes: false, //TODO
                fitOnDoubleClick: true, //TODO
            },
            snap: undefined, //TODO
            template: this.renderTemplateItem.bind(this),
            loadingScreenTemplate: undefined,//TODO
            visibleFrameTemplate: undefined, //TODO
            timeAxis: {
                scale: undefined, //TODO
                step: 1, //TODO
            },
            type: undefined, //TODO
            tooltip: {
                followMouse: false, //TODO
                overflowMethod: 'flip', //TODO
                delay: 500, //TODO
                template: undefined, //TODO
            },
            tooltipOnItemUpdateTime: {
                template: undefined, //TODO
            },
            xss: {
                disabled: false, //TODO
                filterOptions: { //TODO merge
                    'allowList': {
                        'strong': true,
                        'i': true,
                        'b': true,
                        'div': ['class', 'style'],
                        'p': ['class', 'style'],
                        'span': ['class', 'style'],
                        'img': ['class', 'style', 'src', 'title', 'alt', 'width', 'height'],
                    },
                },
            },
            width: '100%', //TODO
            height: '100%', //TODO
            minHeight: undefined, //TODO
            maxHeight: undefined, //TODO
            horizontalScroll: false, //TODO
            verticalScroll: true, //TODO
            zoomable: this.props.model.archInfo.zoomable,
            zoomFriction: 40, //TODO
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
