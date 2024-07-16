/** @odoo-module **/

import {Component} from '@odoo/owl';

export class DashboardColumn extends Component {
    static template = 'pyper_dashboard.DashboardColumn';

    static props = {
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
        attr: {},
    };
}
