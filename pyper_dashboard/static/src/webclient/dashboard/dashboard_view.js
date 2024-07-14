/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {DashboardController} from './dashboard_controller';

export const dashboardView = {
    type: 'form',
    display_name: _t('Dashboards'),
    Controller: DashboardController,

    props: (genericProps, view) => {
        return {
            ...genericProps,
            className: 'pyper_dashboard',
        };
    },
};

registry.category('views').add('dashboard', dashboardView);
