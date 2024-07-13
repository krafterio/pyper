/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {GraphRenderer} from '@web/views/graph/graph_renderer';

patch(GraphRenderer.prototype, {
    get displayButtonSection() {
        return !(undefined !== this.env?.searchModel?.display?.controlPanel && !this.env.searchModel.display.controlPanel);
    },
});
