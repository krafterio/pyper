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
import {Component, onWillStart} from '@odoo/owl';

const {DateTime} = luxon;

export const SCALE_LABELS = {
    day: _t('Day'),
    '2days': _t('2 Days'),
    '3days': _t('3 Days'),
    week: _t('Week'),
    month: _t('Month'),
    year: _t('Year'),
};

export const SCALE_DURATIONS = {
    day: {'days': 1},
    '2days': {'days': 2},
    '3days': {'days': 3},
    week: {'weeks': 1},
    month: {'mouth': 1},
    year: {'years': 1},
};

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
        this.model = useModelWithSampleData(
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
        );

        useSetupView({
            getLocalState: () => this.model.exportedState,
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
        const meta = this.model.meta;
        const scale = meta.archInfo.scale;

        if (this.env.isSmall && ['week', 'month'].includes(scale)) {
            const date = meta.date || DateTime.now();
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

    get weekHeader() {
        const {rangeStart, rangeEnd} = this.model;

        if (rangeStart.year !== rangeEnd.year) {
            return `${rangeStart.toFormat('MMMM')} ${rangeStart.year} - ${rangeEnd.toFormat(
                'MMMM'
            )} ${rangeEnd.year}`;
        } else if (rangeStart.month !== rangeEnd.month) {
            return `${rangeStart.toFormat('MMMM')} - ${rangeEnd.toFormat('MMMM')} ${
                rangeStart.year
            }`;
        }

        return `${rangeStart.toFormat('MMMM')} ${rangeStart.year}`;
    }

    get currentMonth() {
        return `${this.date.toFormat('MMMM')} ${this.date.year}`;
    }

    get currentWeek() {
        return getWeekNumber(this.model.rangeStart);
    }

    /**
     * @returns {any}
     */
    get rendererProps() {
        return {
            model: this.model,
            createRecord: this.createRecord.bind(this),
            editRecord: this.editRecord.bind(this),
            deleteRecord: this.deleteRecord.bind(this),
            setDate: this.setDate.bind(this),
            onItemClick: this.openRecords.bind(this), //TODO keep?
        };
    }

    get scales() {
        return Object.fromEntries(
            this.model.scales.map((s) => [s, {description: SCALE_LABELS[s]}])
        );
    }

    async setScale(scale) {
        await this.model.load({scale});
        browser.sessionStorage.setItem('timeline-scale', this.model.scale);
    }

    async setDate(move) {
        const duration = Object.assign({}, SCALE_DURATIONS[this.model.scale] || SCALE_DURATIONS.day);
        let date = null;

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

        await this.model.load({date});
    }

    onWillStartModel() {}

    createRecord(record) {
        if (!this.model.canCreate) {
            return;
        }

        //TODO
        console.log('createRecord', record);
    }

    async editRecord(record, context = {}, shouldFetchFormViewId = true) {
        if (!this.model.canEdit) {
            return;
        }

        //TODO
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
        //TODO keep?
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
}
