/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {DashboardAction} from '@pyper_dashboard/webclient/dashboard/dashboard_action';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';

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
    },

    get showView() {
        return super.showView && !this.props.isFolded;
    },
});
