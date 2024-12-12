/* @odoo-module */

import {Component} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';
import {_t} from '@web/core/l10n/translation';

export class UrlShareMenu extends Component {
    static template = 'pyper_url_share.UrlShareMenu';

    static props = {};

    setup() {
        super.setup();
        this.notificationService = useService('notification');
    }

    async onClick() {
        const url = window.location.href;

        try {
            await navigator.clipboard.writeText(url);

            this.notificationService.add(
                _t('The link has been copied to the clipboard'),
                {
                    type: 'info',
                },
            );
        } catch (e) {
            this.notificationService.add(
                _t('The link could not be copied to the clipboard'),
                {
                    type: 'danger',
                },
            );
        }
    }
}

registry.category('systray').add(
    'pyper_url_share.url_share_button',
    {Component: UrlShareMenu},
    {sequence: 90},
);
