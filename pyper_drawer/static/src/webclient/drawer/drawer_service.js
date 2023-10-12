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

            restoreMinified() {
                return (cookie.get('drawer_mini') || 'false') === 'true';
            },
        };
    },
};
serviceRegistry.add('drawer', drawerService);
