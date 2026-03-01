/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';

const {DateTime} = luxon;

/**
 * All date range presets. Keys are English identifiers, labels are translatable.
 * Each preset with a handler returns [start, end) given a `now` DateTime instance.
 */
export const DATE_RANGE_PRESETS = [
    {
        key: 'all', 
        label: _t('All'),
    },
    {
        key: 'today', 
        label: _t('Today'),
        handler: (now) => {
            const start = now.startOf('day');
            return [start, start.plus({days: 1})];
        },
    },
    {
        key: 'yesterday', 
        label: _t('Yesterday'),
        handler: (now) => {
            const start = now.startOf('day');
            return [start.minus({days: 1}), start];
        },
    },
    {
        key: 'last_7_days', 
        label: _t('Last 7 days'),
        handler: (now) => {
            const start = now.startOf('day');
            return [start.minus({days: 7}), start];
        },
    },
    {
        key: 'last_30_days', 
        label: _t('Last 30 days'),
        handler: (now) => {
            const start = now.startOf('day');
            return [start.minus({days: 30}), start];
        },
    },
    {
        key: 'month_to_date', 
        label: _t('Month to date'),
        handler: (now) => {
            const start = now.startOf('day');
            return [start.startOf('month'), start.plus({days: 1})];
        },
    },
    {
        key: 'year_to_date', 
        label: _t('Year to date'),
        handler: (now) => {
            const start = now.startOf('day');
            return [start.startOf('year'), start.plus({days: 1})];
        },
    },
    {
        key: 'last_3_months', 
        label: _t('Last 3 months'),
        handler: (now) => {
            const monthStart = now.startOf('month');
            return [monthStart.minus({months: 3}), monthStart];
        }},
    {
        key: 'last_6_months', 
        label: _t('Last 6 months'),
        handler: (now) => {
            const monthStart = now.startOf('month');
            return [monthStart.minus({months: 6}), monthStart];
        },
    },
    {
        key: 'last_12_months', 
        label: _t('Last 12 months'),
        handler: (now) => {
            const monthStart = now.startOf('month');
            return [monthStart.minus({months: 12}), monthStart];
        },
    },
    {
        key: 'this_week', 
        label: _t('This week'),
        handler: (now) => {
            const weekStart = now.startOf('week');
            return [weekStart, weekStart.plus({weeks: 1})];
        },
    },
    {
        key: 'this_month', 
        label: _t('This month'),
        handler: (now) => {
            const monthStart = now.startOf('month');
            return [monthStart, monthStart.plus({months: 1})];
        },
    },
    {
        key: 'this_quarter', 
        label: _t('This quarter'),
        handler: (now) => {
            const quarterStart = now.startOf('quarter');
            return [quarterStart, quarterStart.plus({quarters: 1})];
        },
    },
    {
        key: 'this_year', 
        label: _t('This year'),
        handler: (now) => {
            const yearStart = now.startOf('year');
            return [yearStart, yearStart.plus({years: 1})];
        },
    },
    {
        key: 'last_month', 
        label: _t('Last month'),
        handler: (now) => {
            const monthStart = now.startOf('month');
            return [monthStart.minus({months: 1}), monthStart];
        },
    },
    {
        key: 'last_quarter', 
        label: _t('Last quarter'),
        handler: (now) => {
            const quarterStart = now.startOf('quarter');
            return [quarterStart.minus({quarters: 1}), quarterStart];
        },
    },
    {
        key: 'last_year', 
        label: _t('Last year'),
        handler: (now) => {
            const yearStart = now.startOf('year');
            return [yearStart.minus({years: 1}), yearStart];
        },
    },
    {
        key: 'custom', 
        label: _t('Custom'),
    },
];

/**
 * Compute [start, end) dates for a preset range key.
 * Start is inclusive, end is exclusive.
 * Returns null for 'all', 'custom', or unknown keys.
 *
 * @param {string} rangeKey
 * @returns {[DateTime, DateTime]|null}
 */
export function computeDateRange(rangeKey) {
    const preset = DATE_RANGE_PRESETS.find((p) => p.key === rangeKey);

    if (!preset?.handler) {
        return null;
    }

    return preset.handler(DateTime.now());
}

/**
 * Build a domain clause for the date filter.
 *
 * @param {string} filterField - field name, e.g. "platform_created_at"
 * @param {string} filterFieldType - "date" or "datetime"
 * @param {DateTime} start - inclusive start
 * @param {DateTime} end - exclusive end
 * @returns {Array} domain tuples, e.g. ["&", ["field", ">=", "..."], ["field", "<", "..."]]
 */
export function buildFilterDomain(filterField, filterFieldType, start, end) {
    let startStr, endStr;

    if (filterFieldType === 'datetime') {
        startStr = start.toUTC().toFormat('yyyy-MM-dd HH:mm:ss');
        endStr = end.toUTC().toFormat('yyyy-MM-dd HH:mm:ss');
    } else {
        startStr = start.toFormat('yyyy-MM-dd');
        endStr = end.toFormat('yyyy-MM-dd');
    }

    return ['&', [filterField, '>=', startStr], [filterField, '<', endStr]];
}

/** LocalStorage key prefix for persisting the date range selection. */
export const DATE_RANGE_STORAGE_KEY = 'pyper_dashboard.date_range';

/**
 * Serialize date range state for localStorage.
 *
 * @param {string} rangeKey
 * @param {DateTime|null} customStart
 * @param {DateTime|null} customEnd
 * @returns {string}
 */
export function serializeDateRange(rangeKey, customStart, customEnd) {
    const data = {rangeKey};

    if (rangeKey === 'custom' && customStart && customEnd) {
        data.customStart = customStart.toISO();
        data.customEnd = customEnd.toISO();
    }

    return JSON.stringify(data);
}

/**
 * Deserialize date range state from localStorage.
 *
 * @param {string} json
 * @returns {{rangeKey: string, customStart: DateTime|null, customEnd: DateTime|null}}
 */
export function deserializeDateRange(json) {
    try {
        const data = JSON.parse(json);

        return {
            rangeKey: data.rangeKey || 'all',
            customStart: data.customStart ? DateTime.fromISO(data.customStart) : null,
            customEnd: data.customEnd ? DateTime.fromISO(data.customEnd) : null,
        };
    } catch {
        return {rangeKey: 'all', customStart: null, customEnd: null};
    }
}

/**
 * Get the display label for a date range, including formatted dates for custom ranges.
 *
 * @param {string} rangeKey
 * @param {DateTime|null} customStart
 * @param {DateTime|null} customEnd
 * @returns {string}
 */
export function getDateRangeLabel(rangeKey, customStart, customEnd) {
    if (rangeKey === 'custom' && customStart && customEnd) {
        const fmt = {day: 'numeric', month: 'short', year: 'numeric'};
        return `${customStart.toLocaleString(fmt)} - ${customEnd.toLocaleString(fmt)}`;
    }

    const preset = DATE_RANGE_PRESETS.find((p) => p.key === rangeKey);

    return preset ? preset.label : '';
}
