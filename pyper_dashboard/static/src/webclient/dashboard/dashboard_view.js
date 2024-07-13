/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {DashboardArchParser} from './dashboard_arch_parser';
import {DashboardController} from './dashboard_controller';

export const dashboardView = {
    type: 'form',
    display_name: _t('Dashboard'),
    Controller: DashboardController,

    props: (genericProps, view) => {
        const {arch, info} = genericProps;

        return {
            ...genericProps,
            className: 'pyper_dashboard',
            dashboard: new DashboardArchParser().parse(arch, info.customViewId),
        };
    },
};

registry.category('views').add('dashboard', dashboardView);
