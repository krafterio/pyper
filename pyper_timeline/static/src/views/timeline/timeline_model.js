/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {deserializeDateTime, serializeDateTime} from '@web/core/l10n/dates';
import {localization} from '@web/core/l10n/localization';
import {KeepLast} from '@web/core/utils/concurrency';
import {Model} from '@web/model/model';
import {extractFieldsFromArchInfo} from '@web/model/relational_model/utils';
import {orderByToString} from '@web/search/utils/order_by';
import {Domain} from '@web/core/domain';

export class TimelineModel extends Model {
    static services = ['user'];

    setup(params, {user, orm}) {
        this.user = user;
        this.keepLast = new KeepLast();

        const formViewFromConfig = (this.env.config.views || []).find((view) => view[1] === 'form');
        const formViewIdFromConfig = formViewFromConfig ? formViewFromConfig[0] : false;
        const fieldNodes = params.archInfo.fieldNodes;
        const {activeFields, fields} = extractFieldsFromArchInfo({fieldNodes}, params.fields);

        this.meta = {
            ...params,
            activeFields,
            fields,
            firstDayOfWeek: (localization.weekStart || 0) % 7,
            formViewId: params.archInfo.formViewId || formViewIdFromConfig,
            get scale() {
                return params.archInfo.scale;
            },
            set scale(value) {
                params.archInfo.scale = value;
            }
        };

        this.data = {
            hasCreateRight: null,
            hasWriteRight: null,
            hasUnlinkRight: null,
            range: null,
            groups: [],
            items: [],
        };
    }

    get exportedState() {
        return this.meta;
    }

    get canCreate() {
        return this.meta.archInfo.activeActions.create && this.data.hasCreateRight;
    }

    get canWrite() {
        return this.meta.archInfo.activeActions.edit && this.data.hasWriteRight;
    }

    get canUnlink() {
        return this.meta.archInfo.activeActions.delete && this.data.hasUnlinkRight;
    }

    get scale() {
        return this.meta.archInfo.scale;
    }

    get scales() {
        return this.meta.archInfo.scales;
    }

    get zoomKey() {
        return this.meta.archInfo.zoomKey;
    }

    get date() {
        return this.meta.date;
    }

    get rangeStart() {
        return this.data.range?.start;
    }

    get rangeEnd() {
        return this.data.range?.end;
    }

    get groups() {
        return this.data.groups;
    }

    get items() {
        return this.data.items;
    }

    async load(params) {
        Object.assign(this.meta, params || {});

        if (!this.meta.date) {
            this.meta.date = params.context && params.context.initial_date
                ? deserializeDateTime(params.context.initial_date)
                : luxon.DateTime.local();
        }

        // Prevent picking a scale that is not supported by the view
        if (!this.meta.archInfo.scales.includes(this.meta.archInfo.scale)) {
            this.meta.archInfo.scale = this.meta.archInfo.scales[0];
        }

        const data = {...this.data};

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
                [[this.meta.archInfo.fieldDateStart, '>=', serializeDateTime(data.range.start)]],
                [[this.meta.archInfo.fieldDateStart, '<=', serializeDateTime(data.range.end)]],
            ]),
            Domain.and([
                [[this.meta.archInfo.fieldDateEnd, '>=', serializeDateTime(data.range.start)]],
                [[this.meta.archInfo.fieldDateEnd, '<=', serializeDateTime(data.range.end)]],
            ]),
        ]);
        const domain = Domain.and([this.meta.domain, domainRange]).toList(this.meta.context);

        const res = await this.orm.searchRead(this.meta.resModel, domain, this.meta.archInfo.fieldNames, {
            order: orderByToString(this.meta.orderBy || this.meta.archInfo.defaultOrderBy || []),
            limit: this.meta.archInfo.limit,
            context: {...this.user.context},
        });

        const groupBys = this.meta.groupBy.length > 0 ? this.meta.groupBy : this.meta.archInfo.defaultGroupBy;
        const groups = {};
        const items = [];
        let hasUnassigned = false;

        groups[-1] = {
            id: -1,
            content: _t('Unassigned'),
        };

        res.forEach((item) => {
            let group = -1;

            if (groupBys.length > 0) {
                const groupByField = groupBys[0];
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
                        };
                    }
                }
            }

            if (group === -1) {
                hasUnassigned = true;
            }

            items.push({
                id: item.id,
                group: group,
                start: deserializeDateTime(item[this.meta.archInfo.fieldDateStart]).toJSDate(),
                end: deserializeDateTime(item[this.meta.archInfo.fieldDateEnd]).toJSDate(),
                type: 'range',
                record: {
                    resId: item.id,
                    resModel: this.meta.resModel,
                    model: this,
                    setInvalidField: (fieldName) => {},
                    isFieldInvalid: (fieldName) => false,
                    resetFieldValidity: (fieldName) => {},
                    update: (data) => {},
                    isNew: false,
                    isInEdition: false,
                    isValid: true,
                    evalContext: {},
                    evalContextWithVirtualIds: {},
                    fields: this.meta.fields,
                    data: item,
                },
            });
        });

        // Remove unassigned group if it is empty
        if (!hasUnassigned) {
            delete groups[-1];
        }

        data.groups = Object.values(groups);
        data.items = items;
    }

    computeRange() {
        const {date, firstDayOfWeek} = this.meta;
        const {scale} = this.meta.archInfo;
        let start = date;
        let end = date;

        if (!['2days', '3days', 'week'].includes(scale)) {
            // startOf('week') does not depend on locale and will always give the
            // "Monday" of the week...
            start = start.startOf(scale);
            end = end.endOf(scale);
        }

        if (['week', 'month'].includes(scale)) {
            const currentWeekOffset = (start.weekday - firstDayOfWeek + 7) % 7;
            start = start.minus({days: currentWeekOffset});
            end = start.plus({weeks: scale === 'week' ? 1 : 6, days: -1});
        } else if (['2days', '3days'].includes(scale)) {
            const currentWeekOffset = (start.weekday - firstDayOfWeek + 7) % 7;
            start = start.startOf('day');
            end = start.plus({days: scale === '3days' ? 2 : 1});
        }

        start = start.startOf('day');
        end = end.endOf('day');

        return {start, end};
    }
}
