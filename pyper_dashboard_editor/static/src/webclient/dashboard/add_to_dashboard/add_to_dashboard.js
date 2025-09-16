/** @odoo-module **/

import {orderDashboards} from '@pyper_dashboard/webclient/dashboard/utils';
import {_t} from '@web/core/l10n/translation';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {registry} from '@web/core/registry';
import {useAutofocus, useService} from '@web/core/utils/hooks';
import {Component, onWillStart, useState} from '@odoo/owl';
import {rpc} from "@web/core/network/rpc";
import { user } from "@web/core/user";

const cogMenuRegistry = registry.category('cogMenu');

/**
 * The 'Add to dashboard' menu.
 *
 * Component consisting of a toggle button, a text input and an 'Add' button.
 * The first button is simply used to toggle the component and will determine
 * whether the other elements should be rendered.
 *
 * The input will be given the name (or title) of the view that will be added.
 * Finally, the last button will send the name as well as some of the action
 * properties to the server to add the current view (and its context) to the
 * user's dashboard.
 *
 * This component is only available in actions of type 'ir.actions.act_window'.
 *
 * @extends Component
 */
export class AddToDashboard extends Component {
    static template = 'pyper_dashboard_editor.AddToDashboard';

    static components = {
        Dropdown,
    };

    static props = {};

    setup() {
        this.notification = useService('notification');
        this.orm = useService('orm');
        this.state = useState({
            name: this.env.config.getDisplayName(),
            boards: [],
            selectedBoard: null,
        });

        useAutofocus();

        onWillStart(async () => {
            const boardDomain = [['is_editable', '=', true]];

            if (await user.hasGroup('pyper_dashboard.group_dashboard_admin')) {
                const boards = await this.orm.searchRead('dashboard.dashboard', boardDomain, ['id', 'full_name', 'category_id'], {
                    'order': 'category_sequence asc, sequence asc',
                });
                boards.forEach(obj => {
                    obj.name = obj['full_name'];
                    delete obj['full_name'];
                });
                this.state.boards.push(...orderDashboards(boards));
            }

            this.state.boards.push({
                id: null,
                name: _t('My dashboard'),
            });

            this.selectBoard(this.state.boards.length > 0 ? this.state.boards[0].id : null);
        })
    }

    get boards() {
        return this.state.boards;
    }

    get selectedBoard() {
        return this.state.selectedBoard;
    }

    selectBoard(id) {
        for (let board of this.state.boards || []) {
            if (id === board.id) {
                this.state.selectedBoard = board;
                break;
            }
        }
    }

    async addToDashboard(boardId) {
        const {domain, globalContext} = this.env.searchModel;
        const {context, groupBys, orderBy} = this.env.searchModel.getPreFavoriteValues();
        const limit = this.env?.config?.pagerProps?.limit || false;
        const comparison = this.env.searchModel.comparison;
        const contextToSave = {
            ...Object.fromEntries(
                Object.entries(globalContext).filter(
                    (entry) => !entry[0].startsWith('search_default_')
                )
            ),
            ...context,
            order_by: orderBy,
            group_by: groupBys,
        };

        if (limit) {
            contextToSave.limit = limit;
        }

        if (comparison) {
            contextToSave.comparison = comparison;
        }

        const result = await rpc('/dashboard/add_to_dashboard', {
            action_id: this.env.config.actionId || false,
            context_to_save: contextToSave,
            domain,
            name: this.state.name,
            view_mode: this.env.config.viewType,
            board_id: boardId,
        });

        if (result) {
            this.notification.add(
                _t('Please refresh your browser for the changes to take effect.'),
                {
                    title: _t('“%s” added to dashboard', this.state.name),
                    type: 'warning',
                }
            );
            this.state.name = this.env.config.getDisplayName();
        } else {
            this.notification.add(_t('Could not add filter to dashboard'), {
                type: 'danger',
            });
        }
    }

    /**
     * @param {KeyboardEvent} ev
     */
    onInputKeydown(ev) {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            this.addToDashboard().then();
        }
    }
}

export const addToDashboardItem = {
    Component: AddToDashboard,
    groupNumber: 20,
    isDisplayed: async (env) => {
        if (!await user.hasGroup('pyper_dashboard.group_dashboard_user')) {
            return false;
        }

        const {actionType, actionId, viewType} = env.config;

        return actionType === 'ir.actions.act_window' && actionId && viewType !== 'form';
    },
};

cogMenuRegistry.add('pyper-add-to-dashboard', addToDashboardItem, {sequence: 10});
