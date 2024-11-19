/** @odoo-module **/

import {Component} from '@odoo/owl';

export const LAYOUTS = [
    '1',
    '1-1',
    '1-1-1',
    '1-1-1-1',
    '1-2',
    '2-1',
];

export const DEFAULT_LAYOUT = LAYOUTS[0];

export class DashboardSection extends Component {
    static template = 'pyper_dashboard.DashboardSection';

    static props = {
        title: {
            type: String,
            optional: true,
        },
        layout: {
            type: String,
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
        attr: {},
    };

    get layouts() {
        return LAYOUTS;
    }
}
