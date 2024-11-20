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
        this.dialogService.add(DashboardActionDialog, {
            title: this.props.title,
            saveLabel: _t('Edit'),
            save: async (data) => {
                await this.props.edit(data);
            },
        });
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
