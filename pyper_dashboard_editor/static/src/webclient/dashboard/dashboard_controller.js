/** @odoo-module **/

import {blockDom, useRef} from '@odoo/owl';
import {browser} from '@web/core/browser/browser';
import {_t} from '@web/core/l10n/translation';
import {patch} from '@web/core/utils/patch';
import {renderToString} from '@web/core/utils/render';
import {useSortable} from '@web/core/utils/sortable_owl';
import {createColumnData, createSectionData} from '@pyper_dashboard/webclient/dashboard/dashboard_arch_parser';
import {DashboardController} from '@pyper_dashboard/webclient/dashboard/dashboard_controller';
import {DEFAULT_LAYOUT} from '@pyper_dashboard/webclient/dashboard/dashboard_section';
import {DashboardSectionDialog} from './dashboard_section_dialog';

const xmlSerializer = new XMLSerializer();

patch(DashboardController.prototype, {
    leavedSectionIndex: null, // Use when action is dragged between 2 sections

    setup() {
        super.setup();

        const mainRef = useRef('main');

        this.state.editMode = false;

        useSortable({
            ref: mainRef,
            elements: '.pyper_dashboard--section',
            handle: '.pyper_dashboard--section-header',
            cursor: 'move',
            groups: '.pyper_dashboard--container',
            connectGroups: true,
            enable: () => this.canEdit && this.isEditMode,
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
            enable: () => this.canEdit && this.isEditMode,
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
    },

    get isEditMode() {
        return this.state.editMode;
    },

    get canCreate() {
        return this.dashboard?.activeActions?.create || false;
    },

    get canEdit() {
        if (!this.dashboard?.isEmpty) {
            const editable = !!this.dashboard?.activeActions?.edit || !this.selectedBoard;

            if (this.selectedBoard && !this.selectedBoard.is_editable) {
                return false;
            }

            return editable;
        }

        return !!this.dashboard?.activeActions?.edit;
    },

    get canAdmin() {
        return this.canEdit && super.canAdmin;
    },

    get dashboardClasses() {
        return {
            ...super.dashboardClasses,
            'editable': this.canEdit && this.isEditMode,
        };
    },

    get optionsItems() {
        return [
            {
                id: 'enable_edit_mode',
                label: _t('Enable edit'),
                icon: 'oi-fw oi-fw me-1 fa fa-edit',
                onSelected: () => this.toggleEditMode(),
                isShown: () => !this.isEditMode,
            },
            {
                id: 'disable_edit_mode',
                label: _t('Disable edit'),
                icon: 'oi-fw oi-fw me-1 fa fa-edit',
                onSelected: () => this.toggleEditMode(),
                isShown: () => this.isEditMode,
            },
            {
                id: 'add_section',
                label: _t('Add a section'),
                icon: 'oi-fw oi-fw me-1 fa fa-plus',
                onSelected: () => this.addSection(),
                isShown: () => !this.dashboard?.isEmpty && this.isEditMode,
            },
            ...super.optionsItems,
        ];
    },

    toggleEditMode() {
        this.state.editMode = !this.state.editMode;
    },

    addSection() {
        this.dialogService.add(DashboardSectionDialog, {
            title: this.props.title,
            saveLabel: _t('Add'),
            save: async (data) => {
                this.dashboard.sections.push(createSectionData(DEFAULT_LAYOUT, true, data.title));
                this.saveBoard();
            },
        });
    },

    editSection(section, sectionData) {
        Object.assign(section, {...sectionData});
        this.saveBoard();
    },

    removeSection(sectionIndex) {
        this.dashboard.sections.splice(sectionIndex, 1);

        if (!this.dashboard.isEmpty && this.dashboard.sections.length === 0) {
            this.dashboard.isEmpty = true;
        }

        this.saveBoard();
    },

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
    },

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
    },

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
    },

    toggleAction(action) {
        action.isFolded = !action.isFolded;
        this.saveBoard();
    },

    editAction(action, actionData) {
        Object.assign(action, {...actionData});
        this.saveBoard();
    },

    removeAction(column, action) {
        const index = column.actions.indexOf(action);
        column.actions.splice(index, 1);
        this.saveBoard();
    },

    saveBoard() {
        const templateFn = renderToString.app.getTemplate('pyper_dashboard_editor.Arch');
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
    },

    refreshCanvas() {
        if (document.querySelector('canvas')) {
            // Hack to force charts to be recreated, so they pick up the proper size
            browser.requestAnimationFrame(() => this.render(true));
        }
    },
});
