/** @odoo-module **/

import {Component, useEffect, useState} from '@odoo/owl';
import {Dialog} from '@web/core/dialog/dialog';
import {_t} from '@web/core/l10n/translation';
import {useChildRef} from '@web/core/utils/hooks';

export class DashboardDialogBase extends Component {
    static template = 'pyper_dashboard_editor.DashboardDialogBase';

    static components = {
        Dialog,
    };

    static props = {
        close: Function,
        save: Function,
        cancel: {
            type: Function,
            optional: true,
        },
        dialogTitle: {
            type: String,
            optional: true,
        },
        class: {
            type: String,
            optional: true,
        },
        saveLabel: {
            type: String,
            optional: true,
        },
        cancelLabel: {
            type: String,
            optional: true,
        },
    };

    static defaultProps = {
        saveLabel: _t('Save'),
        cancelLabel: _t('Cancel'),
    }

    setup() {
        this.modalRef = useChildRef();
    }

    get dialogSize() {
        return 'md';
    }

    get formData() {
        return {};
    }

    async save() {
        if (!this.isFormValid()) {
            return;
        }

        await this.props.save(this.formData);
        this.props.close();
    }

    async cancel() {
        if (this.props.cancel) {
            await this.props.cancel();
        }

        this.props.close();
    }

    isFormValid() {
        return false;
    }
}

export const useControlledInput = (initialValue, validate) => {
    const input = useState({
        value: initialValue,
        hasError: false,
    });

    const isValid = () => {
        if (validate(input.value)) {
            return true;
        }
        input.hasError = true;
        return false;
    };

    useEffect(() => {
        input.hasError = false;
    }, () => [input.value]);

    return {
        input,
        isValid,
    };
};
