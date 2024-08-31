/** @odoo-module **/

import {browser} from '@web/core/browser/browser';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {_t} from '@web/core/l10n/translation';
import {useService} from '@web/core/utils/hooks';
import {standardViewProps} from '@web/views/standard_view_props';
import {Component, onWillStart, useState} from '@odoo/owl';
import {View} from '@web/views/view';
import {DashboardAction} from './dashboard_action';
import {DashboardArchParser} from './dashboard_arch_parser';
import {DashboardColumn} from './dashboard_column';
import {DashboardSection} from './dashboard_section';
import {orderDashboards} from './utils';

export class DashboardController extends Component {
    static template = 'pyper_dashboard.DashboardView';

    static components = {
        DashboardSection,
        DashboardColumn,
        DashboardAction,
        Dropdown,
        DropdownItem,
        View,
    };

    static props = {
        ...standardViewProps,
    };

    setup() {
        this.dashboard = useState({});
        this.rpc = useService('rpc');
        this.orm = useService('orm');
        this.router = useService('router');
        this.user = useService('user');
        this.actionService = useService('action');
        this.dialogService = useService('dialog');
        this.state = useState({
            boards: [],
            selectedBoard: null,
            useSwitcher: false,
            isAdmin: false,
        });

        onWillStart(async () => {
            const {arch, info} = this.props;
            Object.assign(this.dashboard, new DashboardArchParser().parse(arch, info.customViewId));

            if (this.dashboard.useSwitcher) {
                const boards = await this.orm.searchRead('dashboard.dashboard', [], ['id', 'name', 'category_id', 'full_name', 'arch', 'is_editable'], {
                    'order': 'category_sequence asc, sequence asc',
                });
                this.state.boards.length = 0;
                this.state.boards.push(...orderDashboards(boards));
                this.selectBoard(this.router?.current?.hash?.board || null);
            }

            if ('dashboard.dashboard' === this.props.resModel) {
                this.state.isAdmin = await this.user.hasGroup('pyper_dashboard.group_dashboard_admin');
            }
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

        if (this.dashboard.useSwitcher && this.state.selectedBoard?.id) {
            browser.setTimeout(() => {
                this.router.replaceState({board: this.state.selectedBoard.id});
            }, 200); // history.pushState is a little async
        }
    }

    actionSettings() {
        this.actionService.doAction('pyper_dashboard.action_dashboard_dashboard_list');
    }
}
