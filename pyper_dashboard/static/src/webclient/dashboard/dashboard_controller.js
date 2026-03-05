/** @odoo-module **/

import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {_t} from '@web/core/l10n/translation';
import {useService} from '@web/core/utils/hooks';
import {standardViewProps} from '@web/views/standard_view_props';
import {Component, onMounted, onWillStart, onWillUnmount, useState} from '@odoo/owl';
import {View} from '@web/views/view';
import {user} from '@web/core/user';
import {browser} from '@web/core/browser/browser';
import {router} from '@web/core/browser/router';
import {DashboardAction} from './dashboard_action';
import {DashboardArchParser} from './dashboard_arch_parser';
import {DashboardColumn} from './dashboard_column';
import {DashboardSection} from './dashboard_section';
import {DateRangePicker} from './date_range_picker';
import {orderDashboards} from './utils';
import {
    computeDateRange,
    buildFilterDomain,
    DATE_RANGE_STORAGE_KEY,
    serializeDateRange,
    deserializeDateRange,
} from './date_range_utils';

const {DateTime} = luxon;

export class DashboardController extends Component {
    static template = 'pyper_dashboard.DashboardView';

    static components = {
        DashboardSection,
        DashboardColumn,
        DashboardAction,
        DateRangePicker,
        Dropdown,
        DropdownItem,
        View,
    };

    static props = {
        ...standardViewProps,
    };

    setup() {
        this.dashboard = useState({});
        this.orm = useService('orm');
        this.actionService = useService('action');
        this.dialogService = useService('dialog');
        this.state = useState({
            boards: [],
            selectedBoard: null,
            useSwitcher: false,
            isAdmin: false,
        });
        this.dateRangeState = useState({
            rangeKey: 'all',
            customStart: null,
            customEnd: null,
        });
        this._autoRefreshTimer = null;

        onWillStart(async () => {
            const {arch, info} = this.props;
            this.actionTitle = this.env.config.getDisplayName?.() || '';
            Object.assign(this.dashboard, new DashboardArchParser().parse(arch, info.customViewId));

            if (this.dashboard.useSwitcher) {
                const boards = await this.orm.searchRead('dashboard.dashboard', [], ['id', 'name', 'category_id', 'full_name', 'arch', 'is_editable', 'auto_refresh', 'refresh_interval'], {
                    'order': 'category_sequence asc, sequence asc',
                });
                this.state.boards.length = 0;
                this.state.boards.push(...orderDashboards(boards));
                this.selectBoard(this.props.resId || null);
            }

            if ('dashboard.dashboard' === this.props.resModel) {
                this.state.isAdmin = await user.hasGroup('pyper_dashboard.group_dashboard_admin');
            }

            this._restoreDateRange(true);
        });

        onMounted(() => {
            this._startAutoRefresh();
        });

        onWillUnmount(() => {
            this._stopAutoRefresh();
        });
    }

    get canAdmin() {
        return this.state.isAdmin;
    }

    get boards() {
        return this.state.boards || [];
    }

    get selectedBoard() {
        return this.state.selectedBoard;
    }

    get dashboardClasses() {
        return {};
    }

    get optionsItems() {
        return [
            {
                id: 'settings',
                label: _t('Settings'),
                icon: 'oi-fw oi-fw me-1 fa fa-gear',
                onSelected: () => this.actionSettings(),
                isShown: () => this.canAdmin,
            },
        ];
    }

    get filteredOptionsItems() {
        return this.optionsItems.filter((item) => {
            return item.isShown && item.isShown();
        });
    }

    get categoryBoards() {
        const categories = {}

        this.boards.forEach(board => {
            const [categoryId, categoryName] = board.category_id ? board.category_id : [0, undefined];

            if (!categories[categoryId]) {
                categories[categoryId] = {
                    id: categoryId,
                    name: categoryName,
                    boards: [],
                };
            }

            categories[categoryId].boards.push(board);
        });

        const emptyCategory = categories[0] ? categories[0] : undefined;
        delete categories[0];
        const values = Object.values(categories);

        if (emptyCategory) {
            values.push(emptyCategory);
        }

        return values;
    }

    /**
     * Check if any action in the dashboard has a filter field defined.
     */
    get hasFilterableActions() {
        if (!this.dashboard.sections) {
            return false;
        }

        return this.dashboard.sections.some((section) =>
            section.columns.some((column) =>
                column.actions.some((action) => !!action.filterField)
            )
        );
    }

    selectBoard(value) {
        if (typeof value === 'number') {
            for (let board of this.boards) {
                if (value === board.id) {
                    this.state.selectedBoard = board;
                    break;
                }
            }
        } else if (typeof value === 'object' && value && value.id) {
            this.state.selectedBoard = value;
        } else {
            this.state.selectedBoard = this.state.boards.length > 0 ? this.state.boards[0] : null;
        }

        const arch = this.state.selectedBoard?.arch || this.props.arch;
        Object.assign(this.dashboard, new DashboardArchParser().parse(arch, this.props.info.customViewId));

        if (this.state.selectedBoard?.id) {
            this.props.updateActionState?.({resId: this.state.selectedBoard.id});
            const displayName = this.actionTitle
                ? `${this.actionTitle} - ${this.state.selectedBoard.name}`
                : this.state.selectedBoard.name;
            this.env.config.setDisplayName?.(displayName);
        }

        this._restoreDateRange();
        this._startAutoRefresh();
    }

    refreshDashboard() {
        DashboardAction.cache = {};
        this.env.bus.trigger('dashboard-refresh');
    }

    actionSettings() {
        this.actionService.doAction('pyper_dashboard.action_dashboard_dashboard_list');
    }

    // ---- Date Range ----

    /**
     * Restore date range state. On initial load (fromUrl=true), reads from URL
     * query params first, then falls back to localStorage. On board switch
     * (fromUrl=false), reads from localStorage only.
     *
     * @param {boolean} [fromUrl=false]
     */
    _restoreDateRange(fromUrl = false) {
        if (fromUrl) {
            const urlState = router.current;

            if (urlState.dateRange && urlState.dateRange !== 'all') {
                this.dateRangeState.rangeKey = urlState.dateRange;

                if (urlState.dateRange === 'custom' && urlState.dateRangeStart && urlState.dateRangeEnd) {
                    this.dateRangeState.customStart = DateTime.fromISO(String(urlState.dateRangeStart));
                    this.dateRangeState.customEnd = DateTime.fromISO(String(urlState.dateRangeEnd));
                } else {
                    this.dateRangeState.customStart = null;
                    this.dateRangeState.customEnd = null;
                }

                this._persistDateRangeToStorage();
                this._pushDateRangeToUrl();
                return;
            }
        }

        // Fallback: localStorage
        const storageKey = this._getDateRangeStorageKey();
        const stored = browser.localStorage.getItem(storageKey);

        if (stored) {
            const {rangeKey, customStart, customEnd} = deserializeDateRange(stored);
            this.dateRangeState.rangeKey = rangeKey;
            this.dateRangeState.customStart = customStart;
            this.dateRangeState.customEnd = customEnd;
        } else {
            this.dateRangeState.rangeKey = 'all';
            this.dateRangeState.customStart = null;
            this.dateRangeState.customEnd = null;
        }

        this._pushDateRangeToUrl();
    }

    /**
     * Get a unique localStorage key for the current dashboard context.
     */
    _getDateRangeStorageKey() {
        const boardId = this.state.selectedBoard?.id || 'default';
        const actionId = this.env.config?.actionId || 'default';

        return `${DATE_RANGE_STORAGE_KEY}.${actionId}.${boardId}`;
    }

    /**
     * Persist current date range to localStorage.
     */
    _persistDateRangeToStorage() {
        const storageKey = this._getDateRangeStorageKey();

        if (this.dateRangeState.rangeKey === 'all') {
            browser.localStorage.removeItem(storageKey);
        } else {
            browser.localStorage.setItem(
                storageKey,
                serializeDateRange(
                    this.dateRangeState.rangeKey,
                    this.dateRangeState.customStart,
                    this.dateRangeState.customEnd,
                ),
            );
        }
    }

    /**
     * Push current date range to URL query params via updateActionState.
     */
    _pushDateRangeToUrl() {
        if (!this.props.updateActionState) {
            return;
        }

        if (this.dateRangeState.rangeKey === 'all') {
            this.props.updateActionState({
                dateRange: undefined,
                dateRangeStart: undefined,
                dateRangeEnd: undefined,
            });
        } else {
            const update = {dateRange: this.dateRangeState.rangeKey};

            if (this.dateRangeState.rangeKey === 'custom'
                && this.dateRangeState.customStart
                && this.dateRangeState.customEnd) {
                update.dateRangeStart = this.dateRangeState.customStart.toISODate();
                update.dateRangeEnd = this.dateRangeState.customEnd.toISODate();
            } else {
                update.dateRangeStart = undefined;
                update.dateRangeEnd = undefined;
            }

            this.props.updateActionState(update);
        }
    }

    /**
     * Called when the user selects a date range from the picker.
     */
    onDateRangeSelect(rangeKey, customStart, customEnd) {
        this.dateRangeState.rangeKey = rangeKey;
        this.dateRangeState.customStart = customStart || null;
        this.dateRangeState.customEnd = customEnd || null;

        this._persistDateRangeToStorage();
        this._pushDateRangeToUrl();
    }

    /**
     * Compute the effective domain for an action, merging the base domain
     * with the date filter domain if applicable.
     *
     * @param {Object} action - action data from arch parser
     * @returns {Array} merged domain
     */
    getEffectiveDomain(action) {
        if (!action.filterField || this.dateRangeState.rangeKey === 'all') {
            return action.domain;
        }

        let range;

        if (this.dateRangeState.rangeKey === 'custom') {
            if (this.dateRangeState.customStart && this.dateRangeState.customEnd) {
                // Custom end is the last selected day (inclusive).
                // Domain end = next day start (exclusive).
                range = [
                    this.dateRangeState.customStart.startOf('day'),
                    this.dateRangeState.customEnd.startOf('day').plus({days: 1}),
                ];
            }
        } else {
            range = computeDateRange(this.dateRangeState.rangeKey);
        }

        if (!range) {
            return action.domain;
        }

        const filterDomain = buildFilterDomain(
            action.filterField,
            action.filterFieldType || 'datetime',
            range[0],
            range[1],
        );

        if (!action.domain || !action.domain.length) {
            return filterDomain;
        }

        return [...action.domain, ...filterDomain];
    }

    // ---- Auto Refresh ----

    _startAutoRefresh() {
        this._stopAutoRefresh();

        const board = this.state.selectedBoard;

        if (!board || !board.auto_refresh) {
            return;
        }

        const interval = (board.refresh_interval || 10) * 1000;

        this._autoRefreshTimer = browser.setInterval(() => {
            this.refreshDashboard();
        }, interval);
    }

    _stopAutoRefresh() {
        if (this._autoRefreshTimer) {
            browser.clearInterval(this._autoRefreshTimer);
            this._autoRefreshTimer = null;
        }
    }
}
