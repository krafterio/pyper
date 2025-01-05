/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {useService} from '@web/core/utils/hooks';
import {patch} from '@web/core/utils/patch';
import {FormController} from '@web/views/form/form_controller';

patch(FormController.prototype, {
    setup() {
        super.setup();
        this.actionService = useService('action');
    },

    getStaticActionMenuItems() {
        const items = super.getStaticActionMenuItems();
        const collectionable = this.model.root.model.config.fields?.collection_ids?.relation === 'ir.collections';

        items['collectionAdd'] = {
            isAvailable: () => collectionable,
            sequence: 100,
            icon: 'fa fa-database',
            description: _t('Add to collection'),
            description: _t('Add to collection'),
            callback: () => this._onCollectionAction('pyper_web_collection.action_ir_collections_wizard_add'),
        };
        items['collectionRemove'] = {
            isAvailable: () => collectionable,
            sequence: 101,
            icon: 'fa fa-database',
            description: _t('Remove from collection'),
            callback: () => this._onCollectionAction('pyper_web_collection.action_ir_collections_wizard_remove'),
        };

        return items;
    },

    async _onCollectionAction(actionName) {
        const resIds = this.model.root.resIds;

        if (resIds.length > 0) {
            await this.actionService.doAction(actionName, {
                additionalContext: {
                    active_action_id: this.actionService.currentController?.action?.id,
                    active_model: this.model.root.resModel,
                    active_id: resIds[0],
                    active_ids: resIds,
                },
            });
        }
    },
});
