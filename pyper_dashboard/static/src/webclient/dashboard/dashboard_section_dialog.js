/** @odoo-module **/

import {Component, reactive, useEffect, useState} from '@odoo/owl';
import {Dialog} from '@web/core/dialog/dialog';
import {_t} from '@web/core/l10n/translation';
import {useChildRef} from '@web/core/utils/hooks';

export class DashboardSectionDialog extends Component {
    static template = 'pyper_dashboard.DashboardSectionDialog';

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
        title: {
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
        dialogTitle: _t('Section'),
        saveLabel: _t('Save'),
        cancelLabel: _t('Cancel'),
    }

    setup() {
        this.modalRef = useChildRef();
        this.title = useControlledInput(this.props.title, value => !!value || !value);
    }

    get formData() {
        return {
            title: this.title.input.value || undefined,
        };
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
        return this.title.isValid();
    }
}

const useControlledInput = (initialValue, validate) => {
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
