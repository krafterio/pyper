/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {DashboardDialogBase, useControlledInput} from './dashboard_dialog';

export class DashboardActionDialog extends DashboardDialogBase {
    static template = 'pyper_dashboard_editor.DashboardActionDialog';

    static props = {
        ...DashboardDialogBase.props,
        title: {
            type: String,
            optional: true,
        },
    };

    static defaultProps = {
        ...DashboardDialogBase.defaultProps,
        dialogTitle: _t('Action'),
    }

    setup() {
        super.setup();
        this.title = useControlledInput(this.props.title, value => !!value || !value);
    }

    get formData() {
        return {
            title: this.title.input.value || undefined,
        };
    }

    isFormValid() {
        return this.title.isValid();
    }
}
