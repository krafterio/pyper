/** @odoo-module **/

import {EventBus} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {KanbanController} from '@web/views/kanban/kanban_controller';

export class MapController extends KanbanController {
    static template = 'pyper_map.MapView';

    static defaultProps = {
        ...KanbanController.defaultProps,
        forceGlobalClick: true,
    };

    setup() {
        super.setup();

        this.bus = new EventBus();
    }

    get modelParams() {
        const params = super.modelParams;
        params.config.resPartnerField = this.props.archInfo.resPartnerField;
        params.config.numbering = this.props.archInfo.numbering;

        return params;
    }

    async openRecord(record, mode) {
        this.bus.trigger('pyper-map-open-record', record);
    }

    /**
     * @param {number[]} ids
     */
    async openRecords(ids) {
        if (ids.length > 1) {
            await this.actionService.doAction({
                type: 'ir.actions.act_window',
                name: this.env.config.getDisplayName() || _t('Untitled'),
                views: [
                    [false, 'list'],
                    [false, 'form'],
                ],
                res_model: this.props.resModel,
                domain: [['id', 'in', ids]],
                target: 'current',
            });
        } else {
            await this.actionService.switchView('form', {resId: ids[0]});
        }
    }
}
