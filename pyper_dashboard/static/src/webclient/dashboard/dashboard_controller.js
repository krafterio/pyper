/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {browser} from '@web/core/browser/browser';
import {ConfirmationDialog} from '@web/core/confirmation_dialog/confirmation_dialog';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {useService} from '@web/core/utils/hooks';
import {renderToString} from '@web/core/utils/render';
import {useSortable} from '@web/core/utils/sortable_owl';
import {standardViewProps} from '@web/views/standard_view_props';
import {blockDom, Component, useState, useRef} from '@odoo/owl';
import {DashboardAction} from './dashboard_action';


const xmlSerializer = new XMLSerializer();

export class DashboardController extends Component {
    static template = 'pyper_dashboard.DashboardView';

    static components = {
        DashboardAction,
        Dropdown,
        DropdownItem,
    };

    static props = {
        ...standardViewProps,
        dashboard: Object,
    };

    setup() {
        this.dashboard = useState(this.props.dashboard);
        this.rpc = useService('rpc');
        this.dialogService = useService('dialog');

        const mainRef = useRef('main');

        useSortable({
            ref: mainRef,
            elements: '.pyper-dashboard-action',
            handle: '.pyper-dashboard-action-header',
            cursor: 'move',
            groups: '.pyper-dashboard-column',
            connectGroups: true,
            onDrop: ({element, previous, parent}) => {
                const fromColIdx = parseInt(element.parentElement.dataset.idx, 10);
                const fromActionIdx = parseInt(element.dataset.idx, 10);
                const toColIdx = parseInt(parent.dataset.idx, 10);
                const toActionIdx = previous ? parseInt(previous.dataset.idx, 10) + 1 : 0;

                if (fromColIdx !== toColIdx) {
                    // To reduce visual flickering
                    element.classList.add('d-none');
                }

                this.moveAction(fromColIdx, fromActionIdx, toColIdx, toActionIdx);
            },
        });
    }

    moveAction(fromColIdx, fromActionIdx, toColIdx, toActionIdx) {
        const action = this.dashboard.columns[fromColIdx].actions[fromActionIdx];

        if (fromColIdx !== toColIdx) {
            // Action moving from a column to another
            this.dashboard.columns[fromColIdx].actions.splice(fromActionIdx, 1);
            this.dashboard.columns[toColIdx].actions.splice(toActionIdx, 0, action);
        } else {
            // Move inside a column
            if (fromActionIdx === toActionIdx) {
                return;
            }

            const actions = this.dashboard.columns[fromColIdx].actions;

            if (fromActionIdx < toActionIdx) {
                actions.splice(toActionIdx + 1, 0, action);
                actions.splice(fromActionIdx, 1);
            } else {
                actions.splice(fromActionIdx, 1);
                actions.splice(toActionIdx, 0, action);
            }
        }

        this.saveBoard();
    }

    selectLayout(layout, save = true) {
        const currentColNbr = this.dashboard.colNumber;
        const nextColNbr = layout.split('-').length;

        if (nextColNbr < currentColNbr) {
            // Need to move all actions in last cols in the last visible col
            const cols = this.dashboard.columns;
            const lastVisibleCol = cols[nextColNbr - 1];

            for (let i = nextColNbr; i < currentColNbr; i++) {
                lastVisibleCol.actions.push(...cols[i].actions);
                cols[i].actions = [];
            }
        }

        this.dashboard.layout = layout;
        this.dashboard.colNumber = nextColNbr;

        if (save) {
            this.saveBoard();
        }

        if (document.querySelector('canvas')) {
            // Horrible hack to force charts to be recreated, so they pick up the
            // proper size. also, no idea why raf is needed :(
            browser.requestAnimationFrame(() => this.render(true));
        }
    }

    closeAction(column, action) {
        this.dialogService.add(ConfirmationDialog, {
            body: _t('Are you sure that you want to remove this item?'),
            confirm: () => {
                const index = column.actions.indexOf(action);
                column.actions.splice(index, 1);
                this.saveBoard();
            },
            cancel: () => {},
        });
    }

    toggleAction(action, save = true) {
        action.isFolded = !action.isFolded;

        if (save) {
            this.saveBoard();
        }
    }

    saveBoard() {
        const templateFn = renderToString.app.getTemplate('pyper_dashboard.Arch');
        const bdom = templateFn(this.dashboard, {});
        const root = document.createElement('rendertostring');
        blockDom.mount(bdom, root);
        const result = xmlSerializer.serializeToString(root);
        const arch = result.slice(result.indexOf("<", 1), result.indexOf("</rendertostring>"));

        this.rpc('/web/view/edit_custom', {
            custom_id: this.dashboard.customViewId,
            arch,
        });
        this.env.bus.trigger('CLEAR-CACHES');
    }
}
