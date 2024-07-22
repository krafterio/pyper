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
import {blockDom, Component, onWillStart, useState, useRef} from '@odoo/owl';
import {View} from '@web/views/view';
import {DashboardAction} from './dashboard_action';
import {createColumnData, createSectionData, DashboardArchParser} from './dashboard_arch_parser';
import {DashboardColumn} from './dashboard_column';
import {DashboardSection, DEFAULT_LAYOUT} from './dashboard_section';
import {DashboardSectionDialog} from './dashboard_section_dialog';

const xmlSerializer = new XMLSerializer();

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
        this.leavedSectionIndex = null; // Use when action is dragged between 2 sections

        const mainRef = useRef('main');

        useSortable({
            ref: mainRef,
            elements: '.pyper_dashboard--section',
            handle: '.pyper_dashboard--section-header',
            cursor: 'move',
            groups: '.pyper_dashboard--container',
            connectGroups: true,
            enable: () => this.canEdit,
            onDrop: ({element, previous}) => {
                const fromIdx = parseInt(element.dataset.idx, 10);
                const toIdx = previous ? parseInt(previous.dataset.idx, 10) + 1 : 0;

                this.moveSection(fromIdx, toIdx);
            },
        });

        useSortable({
            ref: mainRef,
            elements: '.pyper_dashboard--action',
            handle: '.pyper_dashboard--action-header',
            cursor: 'move',
            groups: '.pyper_dashboard--column',
            connectGroups: true,
            enable: () => this.canEdit,
            onGroupLeave: (params) => {
                if (null === this.leavedSectionIndex) {
                    this.leavedSectionIndex = parseInt(params.group.closest('.pyper_dashboard--section').dataset.idx, 10);
                }
            },
            onDrop: ({element, previous, parent}) => {
                const fromSecIdx = this.leavedSectionIndex;
                const fromColIdx = parseInt(element.closest('.pyper_dashboard--column').dataset.idx, 10);
                const fromActionIdx = parseInt(element.dataset.idx, 10);
                const toSecIdx = parseInt(parent.closest('.pyper_dashboard--section').dataset.idx, 10);
                const toColIdx = parseInt(parent.dataset.idx, 10);
                const toActionIdx = previous ? parseInt(previous.dataset.idx, 10) + 1 : 0;
                this.leavedSectionIndex = null;

                if (fromSecIdx !== toSecIdx || fromColIdx !== toColIdx) {
                    // To reduce visual flickering
                    element.classList.add('d-none');
                }

                this.moveAction(fromSecIdx, fromColIdx, fromActionIdx, toSecIdx, toColIdx, toActionIdx);
            },
        });

        onWillStart(async () => {
            const {arch, info} = this.props;
            Object.assign(this.dashboard, new DashboardArchParser().parse(arch, info.customViewId));

            if (this.dashboard.useSwitcher) {
                const boards = await this.orm.searchRead('dashboard.dashboard', [], ['id', 'name', 'arch', 'is_editable']);
                this.state.boards.length = 0;
                this.state.boards.push(...boards);
                this.selectBoard(this.router?.current?.hash?.board || null);
            }

            if ('dashboard.dashboard' === this.props.resModel) {
                this.state.isAdmin = await this.user.hasGroup('pyper_dashboard.group_dashboard_admin');
            }
        });
    }

    get canCreate() {
        return this.dashboard?.activeActions?.create || false;
    }

    get canEdit() {
        if (!this.dashboard?.isEmpty) {
            const editable = !!this.dashboard?.activeActions?.edit || !this.selectedBoard;

            if (this.selectedBoard && !this.selectedBoard.is_editable) {
                return false;
            }

            return editable;
        }

        return !!this.dashboard?.activeActions?.edit;
    }

    get canAdmin() {
        return this.canEdit && this.state.isAdmin;
    }

    get boards() {
        return this.state.boards || [];
    }

    get selectedBoard() {
        return this.state.selectedBoard;
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

    addSection() {
        this.dialogService.add(DashboardSectionDialog, {
            title: this.props.title,
            saveLabel: _t('Add'),
            save: async (data) => {
                this.dashboard.sections.push(createSectionData(DEFAULT_LAYOUT, true, data.title));
                this.saveBoard();
            },
        });
    }

    editSection(section, sectionData) {
        Object.assign(section, {...sectionData});
        this.saveBoard();
    }

    removeSection(sectionIndex) {
        this.dashboard.sections.splice(sectionIndex, 1);

        if (!this.dashboard.isEmpty && this.dashboard.sections.length === 0) {
            this.dashboard.isEmpty = true;
        }

        this.saveBoard();
    }

    actionSettings() {
        this.actionService.doAction('pyper_dashboard.action_dashboard_dashboard_list');
    }

    moveSection(fromIdx, toIdx) {
        if (fromIdx === toIdx) {
            return;
        }

        const section = this.dashboard.sections[fromIdx];
        const sections = this.dashboard.sections;

        if (fromIdx < toIdx) {
            sections.splice(toIdx + 1, 0, section);
            sections.splice(fromIdx, 1);
        } else {
            sections.splice(fromIdx, 1);
            sections.splice(toIdx, 0, section);
        }

        this.saveBoard();
    }

    moveAction(fromSecIdx, fromColIdx, fromActionIdx, toSecIdx, toColIdx, toActionIdx) {
        const action = this.dashboard.sections[fromSecIdx].columns[fromColIdx].actions[fromActionIdx];

        if (fromSecIdx !== toSecIdx || fromColIdx !== toColIdx) {
            // Action moving from a column to another
            this.dashboard.sections[fromSecIdx].columns[fromColIdx].actions.splice(fromActionIdx, 1);
            this.dashboard.sections[toSecIdx].columns[toColIdx].actions.splice(toActionIdx, 0, action);
        } else {
            // Move inside a column
            if (fromActionIdx === toActionIdx) {
                return;
            }

            const actions = this.dashboard.sections[fromSecIdx].columns[fromColIdx].actions;

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

    selectLayout(section, layout) {
        if (section.layout === layout) {
            return;
        }

        const currentColNbr = section.columnNumber;
        const nextColNbr = layout.split('-').length;

        if (nextColNbr < currentColNbr) {
            // Need to move all actions in last cols in the last visible col
            const cols = section.columns;
            const lastVisibleCol = cols[nextColNbr - 1];

            for (let i = nextColNbr; i < currentColNbr; i++) {
                lastVisibleCol.actions.push(...cols[i].actions);
                cols[i].actions = [];
            }
        } else if (nextColNbr > currentColNbr) {
            for (let i = 0; i < (nextColNbr - currentColNbr); ++i) {
                section.columns.push(createColumnData());
            }
        }

        section.layout = layout;
        section.columnNumber = nextColNbr;

        this.saveBoard();
        this.refreshCanvas();
    }

    toggleAction(action) {
        action.isFolded = !action.isFolded;
        this.saveBoard();
    }

    removeAction(column, action) {
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

    refreshCanvas() {
        if (document.querySelector('canvas')) {
            // Horrible hack to force charts to be recreated, so they pick up the
            // proper size. also, no idea why raf is needed :(
            browser.requestAnimationFrame(() => this.render(true));
        }
    }

    saveBoard() {
        const templateFn = renderToString.app.getTemplate('pyper_dashboard.Arch');
        const bdom = templateFn(this.dashboard, {});
        const root = document.createElement('rendertostring');
        blockDom.mount(bdom, root);
        const result = xmlSerializer.serializeToString(root);
        const arch = result.slice(result.indexOf("<", 1), result.indexOf("</rendertostring>"));

        if (this.dashboard.useSwitcher && this.state.selectedBoard?.id) {
            this.state.selectedBoard.arch = arch;
            this.orm.write('dashboard.dashboard', [this.state.selectedBoard.id], {
                arch,
            }).then();
        } else {
            this.rpc('/web/view/edit_custom', {
                custom_id: this.dashboard.customViewId,
                arch,
            }).then();
        }

        this.env.bus.trigger('CLEAR-CACHES');
    }
}
