/** @odoo-module **/

import {Component} from '@odoo/owl';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {ConfirmationDialog} from '@web/core/confirmation_dialog/confirmation_dialog';
import {_t} from '@web/core/l10n/translation';
import {useService} from '@web/core/utils/hooks';
import {DashboardSectionDialog} from './dashboard_section_dialog';

export const LAYOUTS = [
    '1',
    '1-1',
    '1-1-1',
    '1-2',
    '2-1',
];

export const DEFAULT_LAYOUT = LAYOUTS[0];

export class DashboardSection extends Component {
    static template = 'pyper_dashboard.DashboardSection';

    static components = {
        Dropdown,
        DropdownItem,
    };

    static props = {
        selectLayout: {
            type: Function,
        },
        edit: {
            type: Function,
        },
        remove: {
            type: Function,
        },
        title: {
            type: String,
            optional: true,
        },
        layout: {
            type: String,
            optional: true,
        },
        layoutEditable: {
            type: Boolean,
            optional: true,
        },
        attr: {
            type: Object,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    };

    static defaultProps = {
        layout: DEFAULT_LAYOUT,
        layoutEditable: true,
        attr: {},
    };

    setup() {
        super.setup();

        this.dialogService = useService('dialog');
    }

    get layouts() {
        return LAYOUTS;
    }

    editSection() {
        this.dialogService.add(DashboardSectionDialog, {
            title: this.props.title,
            saveLabel: _t('Edit'),
            save: async (data) => {
                await this.props.edit(data);
            },
        });
    }

    deleteSection() {
        this.dialogService.add(ConfirmationDialog, {
            title: _t('Delete'),
            body: _t('Are you sure that you want to remove this section?'),
            confirm: async () => {
                await this.props.remove();
            },
            cancel: () => {},
        });
    }

    selectLayout(layout, save = true) {
        this.props.selectLayout(layout, save);
    }
}
