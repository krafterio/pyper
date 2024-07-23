/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {DashboardAction} from '@pyper_dashboard/webclient/dashboard/dashboard_action';

DashboardAction.props = {
    ...DashboardAction.props,
    toggle: {
        type: Function,
    },
    remove: {
        type: Function,
    },
    foldable: {
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
    foldable: true,
    isFolded: false,
};

patch(DashboardAction.prototype, {
    setup() {
        super.setup();
    },

    get showView() {
        return super.showView && !this.props.isFolded;
    },
});
