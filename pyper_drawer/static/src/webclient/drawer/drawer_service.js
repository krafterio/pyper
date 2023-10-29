/** @odoo-module **/

import {registry} from '@web/core/registry';
import {cookie} from '@web/core/browser/cookie';

const serviceRegistry = registry.category('services');

export const drawerService = {
    start() {
        return {
            saveLocked(locked) {
                cookie.set('drawer_locked', locked);
            },

            restoreLocked() {
                return (cookie.get('drawer_locked') || 'true') === 'true';
            },

            saveMinified(locked) {
                cookie.set('drawer_mini', locked);
            },

            restoreMinified(defaultMinified) {
                defaultMinified = !(defaultMinified in [undefined, 'false', false]);
                const defaultValue = defaultMinified ? 'true' : 'false';

                return (cookie.get('drawer_mini') || defaultValue) === 'true';
            },
        };
    },
};
serviceRegistry.add('drawer', drawerService);
