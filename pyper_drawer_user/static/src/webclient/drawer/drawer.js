/** @odoo-module **/

import {Drawer} from '@pyper_drawer/webclient/drawer/drawer';
import {patch} from '@web/core/utils/patch';
import {registry} from '@web/core/registry';
import {ErrorHandler} from '@web/core/utils/components';

patch(Drawer.prototype, {
    get userDrawerItems() {
        return registry.category('drawer_user')
            .getEntries()
            .map(([key, value]) => ({key, ...value}))
            .filter((item) => ('isDisplayed' in item ? item.isDisplayed(this.env) : true))
    },

    handleItemError(error, item) {
        // remove the faulty component
        item.isDisplayed = () => false;
        Promise.resolve().then(() => {
            throw error;
        });
    }
});

Drawer.components.ErrorHandler = ErrorHandler;
