/** @odoo-module **/

import {Component} from '@odoo/owl';
import {CodeEditor} from '@web/core/code_editor/code_editor';
import {Dialog} from '@web/core/dialog/dialog';
import {_t} from '@web/core/l10n/translation';

export class DashboardArchDialog extends Component {
    static template = 'pyper_dashboard_editor.DashboardArchDialog';

    static components = {
        Dialog,
        CodeEditor,
    };

    static props = {
        close: Function,
        title: {
            type: String,
            optional: true,
        },
        arch: {
            type: String,
        },
        save: {
            type: Function,
            optional: true,
        },
    };

    static defaultProps = {
        title: _t('XML'),
    };

    setup() {
        this.currentArch = this.props.arch;
    }

    onArchChange(value) {
        this.currentArch = value;
    }

    async save() {
        if (this.props.save) {
            await this.props.save(this.currentArch);
        }

        this.props.close();
    }
}
