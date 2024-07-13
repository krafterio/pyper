/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {ListController} from '@web/views/list/list_controller';

patch(ListController.prototype, {
    get modelParams() {
        const params = super.modelParams;

        if (null === params.groupsLimit && this.props.limit && this.props.groupBy?.length > 0) {
            params.groupsLimit = this.props.limit;
            params.limit = null;
        }

        return params;
    },
});
