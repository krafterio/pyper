/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {PivotRenderer} from '@web/views/pivot/pivot_renderer';

patch(PivotRenderer.prototype, {
    get displayButtonSection() {
        return !(undefined !== this.env?.searchModel?.display?.controlPanel && !this.env.searchModel.display.controlPanel);
    },
});
