/** @odoo-module */

import {WebClient} from '@web/webclient/webclient';
import {patch} from '@web/core/utils/patch';

patch(WebClient.prototype, {
    setup() {
        super.setup();
        // Use defaultTitle property if it exists
        this.title.setParts({zopenerp: this.defaultTitle || 'Pyper'});
    }
});
