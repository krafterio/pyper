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
        height: {
            type: String,
            optional: true,
        },
        minHeight: {
            type: String,
            optional: true,
        },
        maxHeight: {
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
        this.height = useControlledInput(this.props.height, value => !value || /^\d+(px|vh)$/.test(value));
        this.minHeight = useControlledInput(this.props.minHeight, value => !value || /^\d+(px|vh)$/.test(value));
        this.maxHeight = useControlledInput(this.props.maxHeight, value => !value || /^\d+(px|vh)$/.test(value));
    }

    get formData() {
        return {
            title: this.title.input.value || undefined,
            height: this.height.input.value || undefined,
            minHeight: this.minHeight.input.value || undefined,
            maxHeight: this.maxHeight.input.value || undefined,
        };
    }

    isFormValid() {
        return this.title.isValid() && this.height.isValid() && this.minHeight.isValid() && this.maxHeight.isValid();
    }
}
