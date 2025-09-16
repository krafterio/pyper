/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {deserializeDate, deserializeDateTime, serializeDateTime} from '@web/core/l10n/dates';
import {localization} from '@web/core/l10n/localization';
import {user} from '@web/core/user';
import {KeepLast, Mutex} from '@web/core/utils/concurrency';
import {Model} from '@web/model/model';
import {extractFieldsFromArchInfo} from '@web/model/relational_model/utils';
import {orderByToString} from '@web/search/utils/order_by';
import {Domain} from '@web/core/domain';
import {markup, useState, reactive} from '@odoo/owl';

const {DateTime} = luxon;

export const EMPTY_GROUP_ID = -1;

export class TimelineModel extends Model {
    static services = ['field'];

    setup(params, services) {
        this.field = services.field;
        this.keepLast = new KeepLast();
        this.mutex = new Mutex();

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
            createItemDefaultDurationMinutes: params.archInfo.createItemDefaultDurationMinutes,
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

    get canEdit() {
        return this.archInfo.activeActions.edit && this.data.hasWriteRight;
    }

    get canDelete() {
        return this.archInfo.activeActions.delete && this.data.hasUnlinkRight;
    }

    get groupBy() {
        return this.meta.groupBy.length > 0 ? this.meta.groupBy : this.archInfo.defaultGroupBy;
    }

    get isGroupByMovable() {
        return this.meta.groupBy.length > 0 ? this.meta.groupBy[0].split(':').length === 1 : true;
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
            const weekStart = this.date.minus({days: currentWeekOffset}).startOf('day').setZone('UTC', {
                keepLocalTime: true,
                keepCalendarTime: true,
            });

            // Saturday, Sunday
            if (this.meta.firstDayOfWeek > 0) {
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

    /**
     * Get record id from group id.
     *
     * @param {Number|String} groupId
     *
     * @returns {Integer|Boolean}
     */
    getGroupRecordId(groupId) {
        for (const group of this.groups) {
            if (group.id === groupId) {
                return group.record.resId;
            }
        }

        return false;
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
                this.orm.call(this.meta.resModel, 'check_access', ['create', false]),
                this.orm.call(this.meta.resModel, 'check_access', ['write', false]),
                this.orm.call(this.meta.resModel, 'check_access', ['unlink', false]),
            ]);

            data.hasCreateRight = resRights[0];
            data.hasWriteRight = resRights[1];
            data.hasUnlinkRight = resRights[2];
        }

        data.range = this.computeRange();

        let domainRange = Domain.and([
            [[this.archInfo.fieldDateStart, '>=', serializeDateTime(data.range.start)]],
            [[this.archInfo.fieldDateStart, '<=', serializeDateTime(data.range.end)]],
        ]);

        if (this.archInfo.fieldDateEnd) {
            domainRange = Domain.or([
                Domain.and([
                    [[this.archInfo.fieldDateStart, '!=', false]],
                    [[this.archInfo.fieldDateEnd, '=', false]],
                    [[this.archInfo.fieldDateStart, '>=', serializeDateTime(data.range.start)]],
                    [[this.archInfo.fieldDateStart, '<=', serializeDateTime(data.range.end)]],
                ]),
                Domain.and([
                    [[this.archInfo.fieldDateStart, '=', false]],
                    [[this.archInfo.fieldDateEnd, '!=', false]],
                    [[this.archInfo.fieldDateEnd, '>=', serializeDateTime(data.range.start)]],
                    [[this.archInfo.fieldDateEnd, '<=', serializeDateTime(data.range.end)]],
                ]),
                Domain.and([
                    [[this.archInfo.fieldDateStart, '!=', false]],
                    [[this.archInfo.fieldDateEnd, '!=', false]],
                    Domain.or([
                        domainRange,
                        [[this.archInfo.fieldDateEnd, '>=', serializeDateTime(data.range.start)]],
                    ]),
                ]),
            ]);
        }

        const domain = Domain.and([this.meta.domain, domainRange]).toList(this.meta.context);
        const readFieldNames = [...this.archInfo.fieldNames];

        // Add group by fields if fields are not defined in template
        this.groupBy.forEach((f) => {
            const n = f.split(':')[0];

            if (!readFieldNames.includes(n)) {
                readFieldNames.push(n);
            }
        });

        const emptyGroupLabel = _t('Unassigned');
        let emptyGroupId = EMPTY_GROUP_ID;
        const groupBys = this.meta.groupBy.length > 0 ? this.meta.groupBy : this.archInfo.defaultGroupBy;
        const groupByField = groupBys.length > 0 ? groupBys[0] : null;
        let groupByModel = undefined;
        const groupByFieldNames = this.meta.archInfo.groupFieldNames[groupByField] || null;
        let groupFields = {};
        let groupByFieldInfo = undefined;
        let groupIds = false;
        const groups = {};
        const items = [];
        let res;

        // Search items
        if (!groupByField) {
            // Search items without groups
            res = [await this.orm.searchRead(this.meta.resModel, domain, readFieldNames, {
                order: orderByToString(this.meta.orderBy || this.archInfo.defaultOrderBy || []),
                limit: this.archInfo.limit,
                context: {...user.context},
            })];
        } else {
            // Search items with groups
            groupByFieldInfo = this.meta.fields[groupByField];

            const groupRes = await this.orm.readGroup(this.meta.resModel, domain, readFieldNames, [groupByField], {
                limit: this.archInfo.limit,
                context: {...user.context},
            });
            const allPromises = [];

            for (const i in groupRes) {
                // Prepare search items for each group
                allPromises.push(new Promise((resolve, reject) => {
                    this.orm.searchRead(this.meta.resModel, groupRes[i].__domain, readFieldNames, {
                        order: orderByToString(this.meta.orderBy || this.archInfo.defaultOrderBy || []),
                        limit: this.archInfo.limit,
                        context: {...user.context},
                    }).then(result => {
                        resolve(result);
                    }).catch((e) => reject(e));
                }));

                // Add group
                let groupByContent = groupRes[i][groupByField];
                let groupById = false;
                const groupByPosition = parseInt(i, 10);

                switch (groupByFieldInfo?.type) {
                    case 'selection':
                        for (const selection of (groupByFieldInfo?.selection || [])) {
                            if (groupByContent === selection[0]) {
                                groupByContent = selection[1];
                                break;
                            }
                        }

                        if (groupByContent === false) {
                            emptyGroupId = groupByPosition;
                            groupByContent = emptyGroupLabel;
                        }

                        break;
                    case 'boolean':
                        emptyGroupId = groupByPosition;
                        groupByContent = groupByContent ? _t('Yes') : _t('No');
                        break;
                    case 'one2many':
                    case 'many2many':
                    case 'many2one':
                        if (this.archInfo.groupTemplates[groupByField]) {
                            groupByModel = groupByFieldInfo?.relation;
                            groupIds = {};
                        }

                        if (Array.isArray(groupByContent)) {
                            groupById = groupByContent[0];
                            groupByContent = groupByContent[1] || groupById;
                        } else if (groupByContent === false) {
                            emptyGroupId = groupByPosition;
                            groupByContent = emptyGroupLabel;
                        }

                        break;
                    default:
                        if (groupByContent === false) {
                            emptyGroupId = groupByPosition;
                            groupByContent = emptyGroupLabel;
                        }

                        break;
                }

                groups[groupByPosition] = this.createGroup({
                    id: groupByPosition,
                    content: groupByContent,
                    notUseGroupTemplate: emptyGroupId !== EMPTY_GROUP_ID,
                    order: 0,
                    record: this.generateRecord(groupByModel, groupById, groupFields, groupByFieldNames, {
                        id: groupById,
                        label: groupByContent,
                    }),
                });
            }

            if (groupByField && groupByModel) {
                Object.assign(groupFields, await this.field.loadFields(groupByModel) || {});
            }

            res = await Promise.all(allPromises);
        }

        // Add unassigned group if it is not defined and force option is enabled
        if (!groups[emptyGroupId] && this.archInfo.forceEmptyGroup && (res.length > 0 || this.meta.archInfo.groupByAllRecords)) {
            groups[emptyGroupId] = this.createGroup({
                id: emptyGroupId,
                content: emptyGroupLabel,
                notUseGroupTemplate: emptyGroupId === EMPTY_GROUP_ID,
                order: emptyGroupId,
                record: this.generateRecord(undefined, false, groupFields, groupByFieldNames, {
                    id: false,
                    label: emptyGroupLabel,
                }),
            });
        }

        for (const i in res) {
            const resItems = res[i];
            const groupByPosition = parseInt(i, 10);

            for (const item of resItems) {
                Object.keys(item).forEach((property) => {
                    const type = this.meta.fields[property]?.type;

                    switch (type) {
                        case 'html':
                            item[property] = item[property] ? markup(item[property]) : false;
                            break;
                        case 'datetime':
                            const valDateTime = deserializeDateTime(item[property]);
                            item[property] = valDateTime.invalid ? undefined : valDateTime;
                            break;
                        case 'date':
                            const valDate = deserializeDate(item[property]);
                            item[property] = valDate.invalid ? undefined : valDate;
                            break;
                        default:
                            break;
                    }
                });

                if (groupIds !== false && Array.isArray(item[groupByField]) && !groupIds[item[groupByField][0]]) {
                    groupIds[item[groupByField][0]] = groupByPosition;
                }

                let itemStartDate = item[this.archInfo.fieldDateStart]?.toJSDate();
                let itemEndDate = item[this.archInfo.fieldDateEnd]?.toJSDate();
                let className = '';
                let hasDate = true;

                if (this.archInfo.fieldColor && item[this.archInfo.fieldColor]) {
                    className += 'o_timeline_color_' + item[this.archInfo.fieldColor];
                }

                // Timeline required the start date
                if (!itemStartDate && itemEndDate) {
                    itemStartDate = itemEndDate;
                    itemEndDate = undefined;
                }

                if (!itemStartDate && !itemEndDate) {
                    hasDate = false;

                    if (this.rangeStart) {
                        itemStartDate = new Date(this.rangeStart.toJSDate().valueOf());
                    } else if (this.rangeEnd) {
                        itemStartDate = new Date(this.rangeEnd.toJSDate().valueOf());
                    } else {
                        itemStartDate = new Date(luxon.DateTime.now().toJSDate().valueOf());
                    }

                    if (this.rangeStart && this.rangeEnd) {
                        itemEndDate = new Date(this.rangeEnd.toJSDate().valueOf());
                    }
                }

                if ((itemEndDate && DateTime.now() >= itemEndDate) || (undefined === itemEndDate && DateTime.now() >= itemStartDate)) {
                    className += ' o_timeline_past_item';
                }

                if (!hasDate) {
                    className += ' o_timeline_no_date';
                }

                items.push(this.createItem({
                    id: groupByPosition + '_' + item.id,
                    group: groupByField ? groupByPosition : EMPTY_GROUP_ID,
                    groupByModel: groupByModel,
                    groupByField: groupByField,
                    start: itemStartDate,
                    end: itemEndDate,
                    type: itemEndDate ? this.archInfo.itemRangeType : this.archInfo.itemType,
                    content: item.display_name || item.id,
                    record: this.generateRecord(this.meta.resModel, item.id, this.meta.fields, this.meta.archInfo.fieldNames, item),
                    className: className.trim(),
                    hasDate,
                }, item));
            }
        }

        // If all records for relational group by must be rendered and no group exists, force the group by model
        if (this.meta.archInfo.groupByAllRecords && !groupByModel && ['one2many', 'many2many', 'many2one'].includes(groupByFieldInfo?.type) && groupByFieldInfo?.relation) {
            groupByModel = groupByFieldInfo?.relation;
            groupIds = {};
            Object.assign(groupFields, await this.field.loadFields(groupByModel) || {});
        }

        if (groupByModel && groupIds && (Object.keys(groupIds).length > 0 || this.meta.archInfo.groupByAllRecords)) {
            const groupDomain = this.meta.archInfo.groupByAllRecords ? [] : [['id', 'in', Object.keys(groupIds)]];
            const groupRes = await this.orm.searchRead(groupByModel, groupDomain, groupByFieldNames || ['display_name'], {
                order: orderByToString(this.archInfo.groupOrderBy[groupByField] || []),
                limit: undefined,
                context: {...user.context},
            });
            let groupOrder = 1;

            groupRes.forEach(group => {
                if (this.meta.archInfo.groupByAllRecords && !groups[groupIds[group.id]]) {
                    groupIds[group.id] = Object.keys(groups).length + 1;
                    groups[groupIds[group.id]] = this.createGroup({
                        id: group.id,
                        content: group[(groupByFieldNames || ['display_name'])[0]],
                        notUseGroupTemplate: false,
                    });
                }

                if (groups[groupIds[group.id]]) {
                    groups[groupIds[group.id]].order = groupOrder;
                    groups[groupIds[group.id]].record = this.generateRecord(groupByModel, group.id, groupFields, groupByFieldNames, group);
                    groups[groupIds[group.id]] = this.updateRecordGroup(groups[groupIds[group.id]]);

                    ++groupOrder;
                }
            });
        }

        // Order of group must be greater than or equal zero
        if (groups[EMPTY_GROUP_ID]) {
            Object.values(groups).forEach(group => {
                if (typeof group.order === 'number') {
                    ++group.order;
                }
            });
        }

        data.groups = Object.values(groups);
        data.items = items;
        data.loading = false;
    }

    /**
     * Allow to override values of created timeline group object.
     *
     * @param {Object} group
     *
     * @returns {Object}
     */
    createGroup(group) {
        return group;
    }

    /**
     * Allow to override values of updated record of timeline group object.
     *
     * @param {Object} group
     *
     * @returns {Object}
     */
    updateRecordGroup(group) {
        return group;
    }

    /**
     * Allow to override values of created timeline item object.
     *
     * @param {Object} item
     * @param {Object} data
     *
     * @returns {Object}
     */
    createItem(item, data) {
        return item;
    }

    generateRecord(resModel, resId, fields, fieldNames, data) {
        // Generate fields and fieldNames for empty group item
        if (null === fieldNames) {
            if (0 === Object.keys(fields).length) {
                Object.keys(data).forEach((key) => {
                    fields[key] = {
                        name: key,
                        type: key === 'id' ? 'number' : 'char',
                    };
                });
            }

            fieldNames = Object.keys(fields);
        }

        return {
            resId,
            resModel,
            model: this,
            setInvalidField: (/* fieldName */) => {},
            isFieldInvalid: (/* fieldName */) => false,
            resetFieldValidity: (/* fieldName */) => {},
            update: (/* updateData */) => {},
            isNew: resId === false,
            isInEdition: false,
            isValid: true,
            evalContext: {},
            evalContextWithVirtualIds: {},
            fields,
            fieldNames,
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
