/** @odoo-module */

import {WebClient} from '@web/webclient/webclient';
import {patch} from '@web/core/utils/patch';
import {onWillDestroy, onWillStart} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';

patch(WebClient.prototype, {
    setup() {
        super.setup();
        this.pyperSetupService = useService('pyper_setup');
        this.title.setParts({zopenerp: this.defaultTitle});

        onWillStart(async () => {
            await this.pyperSetupService.register('web.');
            this.title.setParts({zopenerp: this.pyperSetupService.settings['web.'].web_app_name || this.defaultTitle});
        });

        onWillDestroy(() => {
            this.pyperSetupService.unregister('web.');
        });
    },

    get defaultTitle() {
        return this.pyperSetupService?.appName;
    },
});
