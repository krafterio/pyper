/** @odoo-module **/

import {ConfirmationDialog} from '@web/core/confirmation_dialog/confirmation_dialog';
import {_t} from '@web/core/l10n/translation';
import {patch} from '@web/core/utils/patch';
import {DashboardSection} from '@pyper_dashboard/webclient/dashboard/dashboard_section';
import {DashboardSectionDialog} from './dashboard_section_dialog';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {useService} from '@web/core/utils/hooks';

DashboardSection.components = {
    Dropdown,
    DropdownItem,
};

DashboardSection.props = {
    ...DashboardSection.props,
    selectLayout: {
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
};

DashboardSection.defaultProps = {
    ...DashboardSection.defaultProps,
    layoutEditable: true,
};

patch(DashboardSection.prototype, {
    setup() {
        super.setup();

        this.dialogService = useService('dialog');
    },

    editSection() {
        this.dialogService.add(DashboardSectionDialog, {
            title: this.props.title,
            saveLabel: _t('Edit'),
            save: async (data) => {
                await this.props.edit(data);
            },
        });
    },

    deleteSection() {
        this.dialogService.add(ConfirmationDialog, {
            title: _t('Delete'),
            body: _t('Are you sure that you want to remove this section?'),
            confirm: async () => {
                await this.props.remove();
            },
            cancel: () => {},
        });
    },

    selectLayout(layout, save = true) {
        this.props.selectLayout(layout, save);
    },
});
