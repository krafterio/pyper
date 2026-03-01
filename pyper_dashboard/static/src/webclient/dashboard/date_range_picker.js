/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {useDropdownState} from '@web/core/dropdown/dropdown_hooks';
import {DateTimePicker} from '@web/core/datetime/datetime_picker';
import {_t} from '@web/core/l10n/translation';
import {DATE_RANGE_PRESETS, computeDateRange, getDateRangeLabel} from './date_range_utils';

const {DateTime} = luxon;

export class DateRangePicker extends Component {
    static template = 'pyper_dashboard.DateRangePicker';

    static components = {
        Dropdown,
        DateTimePicker,
    };

    static props = {
        value: {
            type: String,
        },
        customStart: {
            optional: true,
        },
        customEnd: {
            optional: true,
        },
        onSelect: {
            type: Function,
        },
    };

    static defaultProps = {
        customStart: null,
        customEnd: null,
    };

    setup() {
        this.presets = DATE_RANGE_PRESETS;
        this.dropdownState = useDropdownState();

        // Pending state: tracks selection before "Apply" is clicked
        this.pending = useState({
            rangeKey: this.props.value,
            customStart: this.props.customStart,
            customEnd: this.props.customEnd,
            focusedDateIndex: 0,
        });
    }

    get selectedLabel() {
        return getDateRangeLabel(this.props.value, this.props.customStart, this.props.customEnd)
            || _t('All');
    }

    get pendingLabel() {
        return getDateRangeLabel(this.pending.rangeKey, this.pending.customStart, this.pending.customEnd)
            || _t('All');
    }

    get isCustom() {
        return this.pending.rangeKey === 'custom';
    }

    get calendarValue() {
        if (this.isCustom) {
            if (this.pending.customStart && this.pending.customEnd) {
                return [this.pending.customStart, this.pending.customEnd];
            }

            return [DateTime.now().startOf('day'), DateTime.now().startOf('day')];
        }

        const range = computeDateRange(this.pending.rangeKey);

        if (!range) {
            return null;
        }

        // Display range: end is inclusive (subtract 1 day from exclusive end)
        return [range[0], range[1].minus({days: 1})];
    }

    get showCalendar() {
        return this.pending.rangeKey !== 'all';
    }

    onDropdownOpened() {
        // Reset pending state to current props when dropdown opens
        this.pending.rangeKey = this.props.value;
        this.pending.customStart = this.props.customStart;
        this.pending.customEnd = this.props.customEnd;
        this.pending.focusedDateIndex = 0;
    }

    onPresetSelected(rangeKey) {
        this.pending.rangeKey = rangeKey;

        if (rangeKey !== 'custom') {
            this.pending.customStart = null;
            this.pending.customEnd = null;
        } else if (!this.pending.customStart || !this.pending.customEnd) {
            // Default custom range to today
            const todayStart = DateTime.now().startOf('day');
            this.pending.customStart = todayStart;
            this.pending.customEnd = todayStart;
        }

        this.pending.focusedDateIndex = 0;
    }

    onCalendarSelect(value) {
        if (!this.isCustom || !Array.isArray(value)) {
            return;
        }

        this.pending.customStart = value[0];
        this.pending.customEnd = value[1];

        // Toggle focused date index for next selection
        this.pending.focusedDateIndex = this.pending.focusedDateIndex === 0 ? 1 : 0;
    }

    onApply() {
        this.props.onSelect(
            this.pending.rangeKey,
            this.pending.customStart,
            this.pending.customEnd,
        );
        this.dropdownState.close();
    }

    onCancel() {
        this.dropdownState.close();
    }
}
