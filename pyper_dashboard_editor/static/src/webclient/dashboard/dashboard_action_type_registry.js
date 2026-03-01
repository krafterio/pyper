/** @odoo-module **/

import {registry} from '@web/core/registry';
import {_t} from '@web/core/l10n/translation';

export const dashboardActionTypeRegistry = registry.category('dashboard_action_types');

dashboardActionTypeRegistry.add('kpi', {
    label: _t('KPI'),
    sequence: 5,
});

dashboardActionTypeRegistry.add('action', {
    label: _t('Existing Action'),
    sequence: 10,
});

dashboardActionTypeRegistry.add('view', {
    label: _t('Custom View'),
    sequence: 20,
});
