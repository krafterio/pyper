/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {loadJS, loadCSS} from '@web/core/assets';
import {useService} from '@web/core/utils/hooks';
import {useModelWithSampleData} from '@web/model/model';
import {useSetupView} from '@web/views/view_hook';
import {Layout} from '@web/search/layout';
import {SearchBar} from '@web/search/search_bar/search_bar';
import {useSearchBarToggler} from '@web/search/search_bar/search_bar_toggler';
import {CogMenu} from '@web/search/cog_menu/cog_menu';
import {browser} from '@web/core/browser/browser';
import {ViewScaleSelector} from '@web/views/view_components/view_scale_selector';
import {getWeekNumber} from '@web/views/calendar/utils';
import {ConfirmationDialog, deleteConfirmationMessage} from '@web/core/confirmation_dialog/confirmation_dialog';
import {Component, onWillStart, useState} from '@odoo/owl';

const {DateTime} = luxon;

export const SCALES = {
    day: {
        description: _t('Day'),
        duration: {'days': 1},
        zoom: 1000 * 60 * 60 * 24, // About 1 day in milliseconds
        clustering: false,
        force_weekends_visibility: true,
    },
    '2days': {
        description: _t('2 days'),
        duration: {'days': 2},
        zoom: 1000 * 60 * 60 * 24 * 2, // About 2 days in milliseconds
        clustering: false,
        force_weekends_visibility: true,
    },
    '3days': {
        description: _t('3 days'),
        duration: {'days': 3},
        zoom: 1000 * 60 * 60 * 24 * 3, // About 3 days in milliseconds
        clustering: false,
        force_weekends_visibility: true,
    },
    week: {
        description: _t('Week'),
        duration: {'weeks': 1},
        zoom: 1000 * 60 * 60 * 24 * 7, // About 7 days in milliseconds
        clustering: false,
        force_weekends_visibility: false,
    },
    month: {
        description: _t('Month'),
        duration: {'months': 1},
        zoom: 1000 * 60 * 60 * 24 * 31, // About 31 days in milliseconds
        clustering: true,
        force_weekends_visibility: false,
    },
    year: {
        description: _t('Year'),
        duration: {'years': 1},
        zoom: 1000 * 60 * 60 * 24 * 365, // About 365 days in milliseconds
        clustering: true,
        force_weekends_visibility: false,
    },
    custom: {
        description: _t('Custom'),
        duration: null,
        zoom: null,
        clustering: false,
        force_weekends_visibility: false,
    },
};

export const AVAILABLE_SCALES = Object.keys(SCALES).filter((k) => k !== 'custom');

export const MOVE_ACTIONS = {
    next: 'next',
    previous: 'previous',
    today: 'today',
};

export class TimelineController extends Component {
    static template = 'pyper_timeline.TimelineView';

    static components = {
        Layout,
        SearchBar,
        CogMenu,
        ViewScaleSelector,
    };

    setup() {
        this.action = useService('action');

        /** @type {typeof TimelineModel} */
        this.model = useState(useModelWithSampleData(
            this.props.Model,
            {
                archInfo: this.props.archInfo,
                resModel: this.props.resModel,
                domain: this.props.domain,
                fields: this.props.fields,
            },
            {
                onWillStart: this.onWillStartModel.bind(this),
            }
        ));

        this.state = useState({
            // Use the same configuration between calendar and timeline components
            isWeekendVisible: browser.localStorage.getItem('calendar.isWeekendVisible') != null
                ? JSON.parse(browser.localStorage.getItem('calendar.isWeekendVisible'))
                : true,
            customIsWeekendVisible: null,
        });

        useSetupView({
            getLocalState: () => this.model.exportedState,
        });

        onWillStart(() =>
            Promise.all([
                loadJS('/pyper_timeline/static/lib/vis_timeline/vis-timeline-graph2d.js'),
                loadCSS('/pyper_timeline/static/lib/vis_timeline/vis-timeline-graph2d.css'),
            ])
        );

        this.searchBarToggler = useSearchBarToggler();
    }

    get currentDate() {
        const scale = this.model.scale;

        if (this.env.isSmall && ['week', 'month'].includes(scale)) {
            const date = this.model.date || DateTime.now();
            let text = '';

            if (scale === 'week') {
                const startMonth = date.startOf('week');
                const endMonth = date.endOf('week');

                if (startMonth.toFormat('LLL') !== endMonth.toFormat('LLL')) {
                    text = `${startMonth.toFormat("LLL")}-${endMonth.toFormat('LLL')}`;
                } else {
                    text = startMonth.toFormat('LLLL');
                }
            } else if (scale === 'month') {
                text = date.toFormat('LLLL');
            }

            return ` - ${text} ${date.year}`;
        } else {
            return '';
        }
    }

    get date() {
        return this.model.meta.date || DateTime.now();
    }

    get today() {
        return DateTime.now().toFormat('d');
    }

    get currentYear() {
        return this.date.toFormat('y');
    }

    get dayHeader() {
        return `${this.date.toFormat('d')} ${this.date.toFormat('MMMM')} ${this.date.year}`;
    }

    get daysHeader() {
        const {rangeStart, rangeEnd} = this.model;

        if (rangeStart.year !== rangeEnd.year) {
            return `${rangeStart.toFormat('d')} ${rangeStart.toFormat('MMMM')} ${rangeStart.year} - ${rangeEnd.toFormat('d')} ${rangeEnd.toFormat('MMMM')} ${rangeEnd.year}`;
        } else if (rangeStart.month !== rangeEnd.month) {
            return `${rangeStart.toFormat('d')} ${rangeStart.toFormat('MMMM')} - ${rangeEnd.toFormat('d')} ${rangeEnd.toFormat('MMMM')} ${rangeStart.year}`;
        }

        return `${rangeStart.toFormat('d')} - ${rangeEnd.toFormat('d')} ${rangeStart.toFormat('MMMM')} ${rangeStart.year}`;
    }

    get weekHeader() {
        const {rangeStart, rangeEnd} = this.model;

        if (rangeStart.year !== rangeEnd.year) {
            return `${rangeStart.toFormat('MMMM')} ${rangeStart.year} - ${rangeEnd.toFormat('MMMM')} ${rangeEnd.year}`;
        } else if (rangeStart.month !== rangeEnd.month) {
            return `${rangeStart.toFormat('MMMM')} - ${rangeEnd.toFormat('MMMM')} ${rangeStart.year}`;
        }

        return `${rangeStart.toFormat('MMMM')} ${rangeStart.year}`;
    }

    get currentMonth() {
        return `${this.date.toFormat('MMMM')} ${this.date.year}`;
    }

    get currentWeek() {
        return getWeekNumber(this.model.rangeStart);
    }

    get rendererIsWeekendVisible() {
        return this.state.customIsWeekendVisible
            || this.state.isWeekendVisible
            || SCALES[this.model.scale]?.force_weekends_visibility;
    }

    /**
     * @returns {any}
     */
    get rendererProps() {
        return {
            model: this.model,
            isWeekendVisible: this.rendererIsWeekendVisible,
            setRange: this.setRange.bind(this),
            createRecord: this.createRecord.bind(this),
            editRecord: this.editRecord.bind(this),
            deleteRecord: this.deleteRecord.bind(this),
            openRecords: this.openRecords.bind(this),
        };
    }

    get scales() {
        return Object.fromEntries(this.model.archInfo.scales.map((s) => {
            return [s, {...SCALES[s]}];
        }));
    }

    async setScale(scale) {
        if ('custom' === scale) {
            // Custom scale can only set by the timeline
            return;
        }

        this.state.customIsWeekendVisible = null;

        await this.model.load({scale});
        browser.sessionStorage.setItem('timeline-scale', this.model.scale);
    }

    async setDate(move) {
        let duration = Object.assign({}, SCALES[this.model.scale]?.duration || SCALES['day']?.duration);
        let date = null;

        if ('custom' === this.model.scale) {
            const rangeEnd = this.model.rangeEnd || this.model.date || DateTime.local().startOf('day');
            duration = rangeEnd.diff(this.model.date);
        }

        switch (move) {
            case MOVE_ACTIONS.next:
                date = this.model.date.plus(duration);
                break;
            case MOVE_ACTIONS.previous:
                date = this.model.date.minus(duration);
                break;
            case MOVE_ACTIONS.today:
                date = DateTime.local().startOf('day');
                break;
        }

        this.state.customIsWeekendVisible = null;

        await this.model.load({date});
    }

    async setRange(start, end) {
        this.state.customIsWeekendVisible = this.state.isWeekendVisible
            || SCALES[this.model.scale]?.force_weekends_visibility;

        await this.model.load({rangeStart: start, rangeEnd: end});
    }

    async toggleWeekendVisibility() {
        this.state.isWeekendVisible = !this.state.isWeekendVisible;
        browser.localStorage.setItem('calendar.isWeekendVisible', this.state.isWeekendVisible);

        await this.model.load();
    }

    createRecord(record) {
        if (!this.model.canCreate) {
            return;
        }

        //TODO createRecord
        console.log('createRecord', record);
    }

    async editRecord(record, context = {}, shouldFetchFormViewId = true) {
        if (!this.model.canEdit) {
            return;
        }

        //TODO editRecord
        console.log('editRecord', record, context, shouldFetchFormViewId);
    }

    deleteRecord(record) {
        this.displayDialog(ConfirmationDialog, {
            title: _t('Bye-bye, record!'),
            body: deleteConfirmationMessage,
            confirm: () => {
                this.model.unlinkRecord(record.id);
            },
            confirmLabel: _t('Delete'),
            cancel: () => {
                // `ConfirmationDialog` needs this prop to display the cancel button, but we do nothing on cancel.
            },
            cancelLabel: _t('No, keep it'),
        });
    }

    /**
     * Redirects to views when clicked on open button in item popup.
     *
     * @param {number[]} ids
     */
    openRecords(ids) {
        if (ids.length > 1) {
            this.action.doAction({
                type: 'ir.actions.act_window',
                name: this.env.config.getDisplayName() || _t('Untitled'),
                views: [
                    [false, 'list'],
                    [false, 'form'],
                ],
                res_model: this.props.resModel,
                domain: [['id', 'in', ids]],
            });
        } else {
            this.action.switchView('form', {
                resId: ids[0],
            });
        }
    }

    onWillStartModel() {}
}
