/** @odoo-module **/

import {App, Component, onMounted, onWillDestroy, useEffect, useRef} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {useViewCompiler} from '@web/views/view_compiler';
import {TimelineCompiler} from './timeline_compiler';
import {TimelineRecord} from './timeline_record';
import {templates} from '@web/core/assets';


export const SCALE_ZOOMS = {
    day: 1000 * 60 * 60 * 24, // About 1 day in milliseconds
    week: 1000 * 60 * 60 * 24 * 7, // About 7 days in milliseconds
    month: 1000 * 60 * 60 * 24 * 31, // About 31 days in milliseconds
    year: 1000 * 60 * 60 * 24 * 365, // About 365 days in milliseconds
};

export class TimelineRenderer extends Component {
    static template = 'pyper_timeline.TimelineRenderer';

    static props = {
        model: {
            type: Object,
            optional: true,
        },
        createRecord: {
            //TODO
            type: Function,
            optional: true,
        },
        editRecord: {
            //TODO
            type: Function,
            optional: true,
        },
        deleteRecord: {
            //TODO
            type: Function,
            optional: true,
        },
        setDate: {
            //TODO
            type: Function,
            optional: true,
        },
        onItemClick: {
            //TODO keep?
            type: Function,
            optional: true,
        },
    };

    setup() {
        this.uiService = useService('ui');
        this.notificationService = useService('notification');
        this.timelineRef = useRef('timeline');
        this.timeline = null;
        this.rendererItems = new Map();
        this.toRendererItems = new Map();

        const {itemTemplate} = this.props.model.meta.archInfo;
        this.timelineTemplates = useViewCompiler(TimelineCompiler, {
            itemTemplate,
        });

        onMounted(() => {
            this.timeline = new vis.Timeline(this.timelineRef.el, [], [], {});
            this.timeline.on('changed', this.onTimelineChanged.bind(this));
        });

        onWillDestroy(() => {
            this.timeline.off('changed', this.onTimelineChanged.bind(this));
            this.timeline.destroy();
        });

        useEffect(() => {
            this.timeline.setOptions(this.timelineOptions);
        }, () => [this.timelineOptions]);

        useEffect(() => {
            this.onScaleChange();
        }, () => [this.props.model.scale]);

        useEffect(() => {
            this.onItemsChange();
        }, () => [this.props.model.groups, this.props.model.items]);
    }

    get timelineOptions() {
        return {
            align: 'left', //TODO
            autoResize: true, //TODO
            clickToUse: false, //TODO
            configure: false, //TODO
            dataAttributes: [], //TODO
            editable: {
                add: this.props.model.canCreate,
                remove: this.props.model.canUnlink,
                updateGroup: this.props.model.canWrite,
                updateTime: this.props.model.canWrite,
                overrideItems: false, //TODO
            },
            //format: undefined, //TODO
            groupEditable: {
                add: false, //TODO
                remove: false, //TODO
                order: false,
            },
            groupHeightMode: 'auto', //TODO
            groupOrder: 'sequence', //TODO
            //groupOrderSwap: undefined, //TODO
            //groupTemplate: undefined, //TODO
            //hiddenDates: undefined, //TODO
            itemsAlwaysDraggable: {
                item: false, //TODO
                range: false, //TODO
            },
            //locale: undefined, //TODO
            //locales: undefined, //TODO
            longSelectPressTime: 251, //TODO
            moment: vis.moment,
            margin: {
                axis: 20, //TODO
                item: {
                    horizontal: 10, //TODO
                    vertical: 10, //TODO
                },
            },
            //max: undefined, //TODO
            maxMinorChars: 7, //TODO
            //min: undefined, //TODO
            moveable: true, //TODO
            multiselect: false, //TODO
            multiselectPerGroup: false, //TODO
            //onAdd: undefined, //TODO
            //onAddGroup: undefined, //TODO
            //onDropObjectOnItem: undefined, //TODO
            //onInitialDrawComplete: undefined, //TODO
            //onMove: undefined, //TODO
            //onMoveGroup: undefined, //TODO
            //onMoving: undefined, //TODO
            //onRemove: undefined, //TODO
            //onRemoveGroup: undefined, //TODO
            //onUpdate: undefined, //TODO
            //order: undefined, //TODO
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
            selectable: true, //TODO
            sequentialSelection: false, //TODO
            showCurrentTime: true, //TODO
            showMajorLabels: true, //TODO
            showMinorLabels: true, //TODO
            showWeekScale: false, //TODO
            showTooltips: true, //TODO
            stack: true, //TODO
            stackSubgroups: true, //TODO
            cluster: {
                maxItems: 1, //TODO
                //titleTemplate: undefined, //TODO
                clusterCriteria: () => false, //TODO
                showStipes: false, //TODO
                fitOnDoubleClick: true, //TODO
            },
            //snap: null, //TODO
            template: this.renderTemplateItem.bind(this),
            //visibleFrameTemplate: undefined, //TODO
            timeAxis: {
                //scale: undefined, //TODO
                step: 1, //TODO
            },
            //type: undefined, //TODO
            tooltip: {
                followMouse: false, //TODO
                overflowMethod: 'flip', //TODO
                delay: 500, //TODO
                //template: undefined, //TODO
            },
            tooltipOnItemUpdateTime: {
                //template: undefined, //TODO
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
            //minHeight: undefined, //TODO
            //maxHeight: undefined, //TODO
            horizontalScroll: false, //TODO
            verticalScroll: true, //TODO
            zoomable: true, //TODO
            zoomFriction: 40, //TODO
            zoomKey: this.props.model.zoomKey,
            zoomMax: SCALE_ZOOMS[this.props.model.meta.archInfo?.scales[this.props.model.meta?.archInfo?.scales?.length - 1] || 'year'],
            zoomMin: SCALE_ZOOMS[this.props.model.meta?.archInfo?.scales[0] || 'day'],
            start: this.props.model.rangeStart.toJSDate(),
            end: this.props.model.rangeEnd.toJSDate(),
        };
    }

    renderTemplateItem(item, element) {
        if (!this.rendererItems.has(element)) {
            const rendererItem = {
                item,
                mounted: false,
                app: new App(TimelineRecord, {
                    env: this.constructor.env,
                    props: {
                        archInfo: this.props.model.meta.archInfo,
                        Compiler: TimelineCompiler,
                        readonly: false, //TODO
                        record: item.record,
                        templates: this.timelineTemplates,
                    },
                    templates: templates,
                }),
            };

            this.rendererItems.set(element, rendererItem);
            this.toRendererItems.set(element, rendererItem);
        }
    }

    onScaleChange() {
        this.timeline.setWindow(this.props.model.rangeStart.toJSDate(), this.props.model.rangeEnd.toJSDate());
    }

    resetRendererItems() {
        this.rendererItems.forEach((rendererItem, element) => {
            if (rendererItem.app && rendererItem.mounted) {
                rendererItem.app.destroy();
            }
        });

        this.rendererItems.clear();
        this.toRendererItems.clear();
    }

    onTimelineChanged() {
        const renderedElements = [];

        this.toRendererItems.forEach((rendererItem, element) => {
            if (!rendererItem.mounted && document.contains(element)) {
                rendererItem.app.mount(element).then();
                rendererItem.mounted = true;
                renderedElements.push(element);
            }
        });

        renderedElements.forEach((element) => {
            this.toRendererItems.delete(element);
        });
    }

    onItemsChange() {
        console.log('onItemsChange', this);

        this.resetRendererItems();
        this.timeline.setData({
            groups: new vis.DataSet(this.props.model.groups),
            //TODO restore after test
            items: new vis.DataSet(this.props.model.items),
            /*items: new vis.DataSet([
                {
                    id: 2798,
                    start: deserializeDateTime('2024-04-30 14:00:00').toJSDate(),
                    end: deserializeDateTime('2024-04-30 15:00:00').toJSDate(),
                    group: 13,
                    record: {
                        resId: 2798,
                        resModel: this.props.model.meta.resId,
                        model: this.props.model,
                        setInvalidField: (fieldName) => {},
                        isFieldInvalid: (fieldName) => false,
                        resetFieldValidity: (fieldName) => {},
                        update: (data) => {},
                        isNew: false,
                        isInEdition: false,
                        isValid: true,
                        evalContext: {},
                        evalContextWithVirtualIds: {},
                        fields: this.props.model.meta.fields,
                        data: {
                            id: 2798,
                            display_name: '[AHMED] #J2798',
                            name: 'J2798',
                            scheduled_start: '2024-04-30 14:00:00',
                            scheduled_finish: '2024-04-30 15:00:00',
                            user_id: [
                                13,
                                'AHMED',
                            ],
                            write_date: '2024-04-30 15:00:00',
                        },
                    },
                }
            ]),*/
        });
    }
}
