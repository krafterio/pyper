/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {deserializeDate, deserializeDateTime, serializeDateTime} from '@web/core/l10n/dates';
import {localization} from '@web/core/l10n/localization';
import {KeepLast} from '@web/core/utils/concurrency';
import {Model} from '@web/model/model';
import {extractFieldsFromArchInfo} from '@web/model/relational_model/utils';
import {orderByToString} from '@web/search/utils/order_by';
import {Domain} from '@web/core/domain';
import {useState, reactive} from '@odoo/owl';

const {DateTime} = luxon;

export class TimelineModel extends Model {
    static services = ['user', 'field'];

    setup(params, services) {
        this.user = services.user;
        this.field = services.field;
        this.keepLast = new KeepLast();

        const formViewFromConfig = (this.env.config.views || []).find((view) => view[1] === 'form');
        const formViewIdFromConfig = formViewFromConfig ? formViewFromConfig[0] : false;
        const fieldNodes = params.archInfo.fieldNodes;
        const {activeFields, fields} = extractFieldsFromArchInfo({fieldNodes}, params.fields);

        this.meta = useState({
            ...params,
            activeFields,
            fields,
            firstDayOfWeek: (localization.weekStart || 0) % 7,
            formViewId: params.archInfo.formViewId || formViewIdFromConfig,
            scale: params.archInfo.scales.includes(params.archInfo.scale)
                ? params.archInfo.scale
                : params.archInfo.scales[0],
            customRangeStart: null,
            customRangeEnd: null,
        });

        this.data = {
            hasCreateRight: null,
            hasWriteRight: null,
            hasUnlinkRight: null,
            range: null,
            groups: [],
            items: [],
            loading: false,
        };
    }

    get exportedState() {
        return this.meta;
    }

    get loading() {
        return this.data.loading;
    }

    get archInfo() {
        return this.meta.archInfo;
    }

    get canCreate() {
        return this.archInfo.activeActions.create && this.data.hasCreateRight;
    }

    get canWrite() {
        return this.archInfo.activeActions.edit && this.data.hasWriteRight;
    }

    get canUnlink() {
        return this.archInfo.activeActions.delete && this.data.hasUnlinkRight;
    }

    get groupBy() {
        return this.meta.groupBy.length > 0 ? this.meta.groupBy : this.archInfo.defaultGroupBy;
    }

    get scale() {
        return this.meta.scale;
    }

    set scale(value) {
        Object.assign(this.meta, this._prepareSetScale(value));
        this.data.range = this.computeRange();
    }

    get date() {
        return this.meta.date;
    }

    set date(value) {
        Object.assign(this.meta, this._prepareSetDate(value));
        this.data.range = this.computeRange();
    }

    get rangeStart() {
        return this.data.range?.start;
    }

    get rangeEnd() {
        return this.data.range?.end;
    }

    get weekends() {
        const weekends = [];

        if (this.date) {
            const currentWeekOffset = (this.date.weekday - this.meta.firstDayOfWeek + 7) % 7;
            const weekStart = this.date.minus({days: currentWeekOffset}).startOf('day');

            // Saturday, Sunday
            if (currentWeekOffset > 0) {
                weekends.push(weekStart.plus({weeks: 1, days: -2}), weekStart.plus({weeks: 1, days: -1}));
            } else {
                weekends.push(weekStart, weekStart.plus({weeks: 1, days: -1}));
            }
        }

        return weekends;
    }

    get groups() {
        return this.data.groups;
    }

    get items() {
        return this.data.items;
    }

    async load(params) {
        this.data.loading = true;
        params = params || {};
        const meta = {};

        if (params.date) {
            Object.assign(meta, this._prepareSetDate(params.date));
            delete params.date;
        }

        if (params.scale) {
            Object.assign(meta, this._prepareSetScale(params.scale));
            delete params.scale;
        }

        if (params.rangeStart || params.rangeEnd) {
            Object.assign(meta, {
                scale: 'custom',
                customRangeStart: params.rangeStart || DateTime.local(),
                customRangeEnd: params.rangeEnd || DateTime.local(),
            });

            if (!this.date) {
                Object.assign(meta, this._prepareSetDate(this.meta.customRangeStart));
            }

            delete params.rangeStart;
            delete params.rangeEnd;
        }

        if (!this.date) {
            // Initialize the date with initial_date in context or use current time
            const initDate = params.context && params.context.initial_date
                ? deserializeDateTime(params.context.initial_date)
                : DateTime.local();
            Object.assign(meta, this._prepareSetDate(initDate));
        }

        const data = {...this.data};
        Object.assign(Object.assign(this.meta, meta), params);

        await this.keepLast.add(this.updateData(data));

        this.data = data;
        this.notify();
    }

    async updateData(data) {
        if (data.hasCreateRight === null || data.hasWriteRight === null || data.hasUnlinkRight === null) {
            const resRights = await Promise.all([
                this.orm.call(this.meta.resModel, 'check_access_rights', ['create', false]),
                this.orm.call(this.meta.resModel, 'check_access_rights', ['write', false]),
                this.orm.call(this.meta.resModel, 'check_access_rights', ['unlink', false]),
            ]);

            data.hasCreateRight = resRights[0];
            data.hasWriteRight = resRights[1];
            data.hasUnlinkRight = resRights[2];
        }

        data.range = this.computeRange();

        const domainRange = Domain.or([
            Domain.and([
                [[this.archInfo.fieldDateStart, '>=', serializeDateTime(data.range.start)]],
                [[this.archInfo.fieldDateStart, '<=', serializeDateTime(data.range.end)]],
            ]),
            Domain.and([
                [[this.archInfo.fieldDateEnd, '>=', serializeDateTime(data.range.start)]],
                [[this.archInfo.fieldDateEnd, '<=', serializeDateTime(data.range.end)]],
            ]),
        ]);
        const domain = Domain.and([this.meta.domain, domainRange]).toList(this.meta.context);

        const res = await this.orm.searchRead(this.meta.resModel, domain, this.archInfo.fieldNames, {
            order: orderByToString(this.meta.orderBy || this.archInfo.defaultOrderBy || []),
            limit: this.archInfo.limit,
            context: {...this.user.context},
        });

        const groupBys = this.meta.groupBy.length > 0 ? this.meta.groupBy : this.archInfo.defaultGroupBy;
        const groupByField = groupBys.length > 0 ? groupBys[0] : null;
        const groupByModel = this.meta.archInfo.groupModels[groupByField] || null;
        const groupByFieldNames = this.meta.archInfo.groupFieldNames[groupByField] || null;
        let groupFields = {};
        const groups = {};
        const items = [];
        let hasUnassigned = false;

        if (groupByField && groupByModel) {
            Object.assign(groupFields, await this.field.loadFields(groupByModel) || {});
        }

        const emptyGroupLabel = _t('Unassigned');
        groups[-1] = {
            id: -1,
            content: emptyGroupLabel,
            record: {
                label: emptyGroupLabel,
            },
            record: this.generateRecord(undefined, -1, groupFields, {
                id: -1,
                label: emptyGroupLabel,
            }),
        };

        res.forEach((item) => {
            let group = -1;

            if (groupByField && groupByModel) {
                const groupByValue = item[groupByField];

                if (undefined !== groupByValue) {
                    let groupById = groupByValue;
                    let groupByContent = groupById;

                    if (Array.isArray(groupByValue)) {
                        groupById = groupByValue[0];
                        groupByContent = groupByValue[1] || groupById;
                    }

                    group = groupById;

                    if (!groups[groupById]) {
                        groups[groupById] = {
                            id: groupById,
                            content: groupByContent,
                            order: Object.values(groups).length,
                            record: this.generateRecord(groupByModel, groupById, groupFields, {
                                id: groupById,
                                label: groupByContent,
                            }),
                        };
                    }
                }
            }

            if (group === -1) {
                hasUnassigned = true;
            }

            Object.keys(item).forEach((property) => {
                const type = this.meta.fields[property]?.type;

                switch (type) {
                    case 'datetime':
                        item[property] = deserializeDateTime(item[property]);
                        break;
                    case 'date':
                        item[property] = deserializeDate(item[property]);
                        break;
                    default:
                        break;
                }
            });

            items.push({
                id: item.id,
                group: group,
                start: item[this.archInfo.fieldDateStart].toJSDate(),
                end: item[this.archInfo.fieldDateEnd].toJSDate(),
                type: 'range',
                content: item.display_name || item.id,
                record: this.generateRecord(this.meta.resModel, item.id, this.meta.fields, item),
            });
        });

        // Remove unassigned group if it is empty
        if (!hasUnassigned) {
            delete groups[-1];
        }

        // Search records of groups
        const groupIds = Object.keys(groups);

        if (groupByField && groupByModel && groupByFieldNames) {
            const groupDomain = [['id', 'in', groupIds]];
            const groupRes = await this.orm.searchRead(groupByModel, groupDomain, groupByFieldNames, {
                order: 'id',
                limit: undefined,
                context: {...this.user.context},
            });

            groupRes.forEach(group => {
                if (groups[group.id]) {
                    groups[group.id].record = this.generateRecord(groupByModel, group.id, groupFields, group);
                }
            });
        }

        data.groups = Object.values(groups);
        data.items = items;
        data.loading = false;
    }

    generateRecord(resModel, resId, fields, data) {
        return {
            resId,
            resModel,
            model: this,
            setInvalidField: (fieldName) => {},
            isFieldInvalid: (fieldName) => false,
            resetFieldValidity: (fieldName) => {},
            update: (updateData) => {},
            isNew: false,
            isInEdition: false,
            isValid: true,
            evalContext: {},
            evalContextWithVirtualIds: {},
            fields,
            data: reactive(data),
        };
    }

    computeRange() {
        const {date, firstDayOfWeek, scale, customRangeStart, customRangeEnd} = this.meta;
        let start = date;
        let end = date;

        if (!['2days', '3days', 'week', 'custom'].includes(scale)) {
            // startOf('week') does not depend on locale and will always give the
            // "Monday" of the week...
            start = start.startOf(scale);
            end = end.endOf(scale);
        }

        const currentWeekOffset = (start.weekday - firstDayOfWeek + 7) % 7;

        if (scale === '2days') {
            start = start.startOf('day');
            end = start.plus({days: 1});
        } else if (scale === '3days') {
            start = start.startOf('day');
            end = start.plus({days: 2});
        } else if (scale === 'week') {
            start = start.minus({days: currentWeekOffset});
            end = start.plus({weeks: 1, days: -1});
        } else if (scale === 'month') {
            start = start.minus({days: currentWeekOffset});
            end = end.endOf('week');
        } else if (scale === 'custom') {
            start = customRangeStart;
            end = customRangeEnd;

            if (!start) {
                start = date;
            }

            if (!end) {
                end = DateTime.fromJSDate(start.toJSDate());
            }
        }

        if (scale !== 'custom') {
            start = start.startOf('day');
            end = end.endOf('day');
        }

        return {start, end};
    }

    _prepareSetScale(value) {
        // Prevent picking a scale that is not supported by the view
        if (!this.archInfo.scales.includes(value)) {
            value = this.archInfo.scales[0];
        }

        return {
            customRangeStart: null,
            customRangeEnd: null,
            scale: value,
        };
    }

    _prepareSetDate(value) {
        const meta = {
            date: value,
        };

        if (this.scale === 'custom' && this.meta.customRangeStart && this.meta.customRangeEnd) {
            const duration = this.meta.customRangeEnd.diff(this.meta.customRangeStart);
            meta.customRangeStart = meta.date;
            meta.customRangeEnd = meta.customRangeStart.plus(duration);
        }

        return meta;
    }
}
