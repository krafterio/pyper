/** @odoo-module **/

import {ConfirmationDialog} from '@web/core/confirmation_dialog/confirmation_dialog';
import {_t} from '@web/core/l10n/translation';
import {patch} from '@web/core/utils/patch';
import {DashboardAction} from '@pyper_dashboard/webclient/dashboard/dashboard_action';
import {DashboardActionDialog} from './dashboard_action_dialog';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {useService} from '@web/core/utils/hooks';

DashboardAction.components = {
    ...DashboardAction.components,
    Dropdown,
    DropdownItem,
};

DashboardAction.props = {
    ...DashboardAction.props,
    toggle: {
        type: Function,
    },
    edit: {
        type: Function,
    },
    duplicate: {
        type: Function,
    },
    remove: {
        type: Function,
    },
    layoutEditable: {
        type: Boolean,
        optional: true,
    },
    isFolded: {
        type: Boolean,
        optional: true,
    },
    filterField: {
        type: String,
        optional: true,
    },
    filterFieldType: {
        type: String,
        optional: true,
    },
    actionData: {
        type: Object,
        optional: true,
    },
    onArchSave: {
        type: Function,
        optional: true,
    },
};

DashboardAction.defaultProps = {
    ...DashboardAction.defaultProps,
    layoutEditable: false,
    isFolded: false,
};

patch(DashboardAction.prototype, {
    setup() {
        super.setup();

        this.dialogService = useService('dialog');
    },

    get showView() {
        return super.showView && !this.props.isFolded;
    },

    editAction() {
        let type;

        if (this.props.type === 'kpi') {
            type = 'kpi';
        } else {
            type = this.props.resModel ? 'view' : 'action';
        }

        this.dialogService.add(DashboardActionDialog, {
            type,
            actionId: this.props.actionId,
            resModel: this.props.resModel,
            viewMode: this.props.viewMode,
            context: this.props.context,
            domain: this.props.domain,
            title: this.props.title,
            icon: this.props.icon,
            height: this.props.height,
            minHeight: this.props.minHeight,
            maxHeight: this.props.maxHeight,
            filterField: this.props.filterField,
            filterFieldType: this.props.filterFieldType,
            actionData: this.props.actionData,
            saveLabel: _t('Edit'),
            save: async (data) => {
                await this.props.edit(data);
            },
            onArchSave: (xml) => {
                this.props.onArchSave?.(xml);
            },
        });
    },

    duplicateAction() {
        this.props.duplicate();
    },

    deleteAction() {
        this.dialogService.add(ConfirmationDialog, {
            title: _t('Delete'),
            body: _t('Are you sure that you want to remove this item?'),
            confirm: async () => {
                await this.props.remove();
            },
            cancel: () => {},
        });
    },
});
