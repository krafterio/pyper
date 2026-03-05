/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {useService} from '@web/core/utils/hooks';
import {DashboardArchDialog} from './dashboard_arch_dialog';
import {DashboardDialogBase, useControlledInput} from './dashboard_dialog';
import {renderSectionArch} from './dashboard_arch_utils';

export class DashboardSectionDialog extends DashboardDialogBase {
    static template = 'pyper_dashboard_editor.DashboardSectionDialog';

    static props = {
        ...DashboardDialogBase.props,
        title: {
            type: String,
            optional: true,
        },
        sectionData: {
            type: Object,
            optional: true,
        },
        onArchSave: {
            type: Function,
            optional: true,
        },
    };

    static defaultProps = {
        ...DashboardDialogBase.defaultProps,
        dialogTitle: _t('Section'),
    }

    setup() {
        super.setup();
        this.dialogService = useService('dialog');
        this.title = useControlledInput(this.props.title, value => !!value || !value);
    }

    get isDebugMode() {
        return Boolean(odoo.debug);
    }

    get formData() {
        return {
            title: this.title.input.value || undefined,
        };
    }

    isFormValid() {
        return this.title.isValid();
    }

    showArchDialog() {
        const section = this.props.sectionData;

        if (!section) {
            return;
        }

        this.dialogService.add(DashboardArchDialog, {
            title: _t('Section XML'),
            arch: renderSectionArch(section),
            save: (xml) => {
                this.props.onArchSave?.(xml);
                this.props.close();
            },
        });
    }
}
