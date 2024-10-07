/* @odoo-module */

import {Component} from '@odoo/owl';
import {registry} from '@web/core/registry';


export class SystrayURLShare extends Component {
    static template = 'pyper_url_share.SystrayButton';

    async onClick() {
        const url = window.location.href;
        try {
            await navigator.clipboard.writeText(url);
            this.showNotification("L'URL a été copiée !");
        } catch (err) {
            console.error('Erreur lors de la copie: ', err);
            this.showNotification("Erreur lors de la copie de l'URL.");
        }
    }

    showNotification(message) {
        const notification = document.createElement("div");
        notification.className = "url-copy-notification";
        notification.innerText = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}
registry
    .category('systray')
    .add('pyper_url_share.systray_button', {Component: SystrayURLShare}, {sequence: 100})
;
