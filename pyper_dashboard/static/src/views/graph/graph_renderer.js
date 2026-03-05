/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {GraphRenderer} from '@web/views/graph/graph_renderer';

patch(GraphRenderer.prototype, {
    get displayButtonSection() {
        return !(undefined !== this.env?.searchModel?.display?.controlPanel && !this.env.searchModel.display.controlPanel);
    },

    renderChart() {
        if (this.chart && this.canvasRef.el && this.chart.canvas?.isConnected) {
            const config = this.getChartConfig();

            if (this.chart.config.type === config.type) {
                const dashboardState = this.env.dashboardState;
                const skipAnimation = dashboardState?.skipAnimation;

                this.chart.data = config.data;
                this.chart.options = config.options;
                this.chart.update(skipAnimation ? 'none' : undefined);

                if (skipAnimation) {
                    dashboardState.skipAnimation = false;
                }

                return;
            }
        }

        super.renderChart();
    },
});
