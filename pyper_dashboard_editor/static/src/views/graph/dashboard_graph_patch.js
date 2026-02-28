/** @odoo-module **/

import {DASHBOARD_PREVIEW_MODE, GRAPH_CONTEXT_KEYS} from '@pyper_dashboard_editor/webclient/dashboard/dashboard_preview_constants';
import {GraphModel} from '@web/views/graph/graph_model';
import {patch} from '@web/core/utils/patch';

patch(GraphModel.prototype, {
    async load(searchParams) {
        await super.load(searchParams);

        // In preview mode, after the initial build has used the graph context keys,
        // remove them from the cached searchParams so that subsequent _buildMetaData
        // calls (e.g. from measure changes) don't override interactive mode/measure choices
        if (this.env?.[DASHBOARD_PREVIEW_MODE]) {
            for (const key of GRAPH_CONTEXT_KEYS) {
                delete this.searchParams.context[key];
            }
        }
    },
});
