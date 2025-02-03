/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {GraphRenderer} from '@web/views/graph/graph_renderer';

const rootStyles = window.getComputedStyle(document.documentElement);

const CUSTOM_COLORS_BRIGHT = [
    rootStyles.getPropertyValue('--primary').trim() || '#262626',
    rootStyles.getPropertyValue('--primary-dark').trim() || '#191919',
    '#5fb7ff',
    '#e6c19b',
    '#82ba82',
    '#b5e1ac',
    '#f48787',
    '#ff9896',
    '#9467bd',
    '#c5b0d5',
    '#e4c0e1',
    '#c49c94',
    '#e377c2',
    '#dcd0d9',
    '#7f7f7f',
    '#c7c7c7',
    '#bcbd22',
    '#dbdb8d',
    '#17becf',
    '#a5d8d7',
];

const CUSTOM_COLORS_DARK = [
    rootStyles.getPropertyValue('--primary').trim() || '#262626',
    rootStyles.getPropertyValue('--primary-dark').trim() || '#191919',
    '#5fb7ff',
    '#e6c19b',
    '#82ba82',
    '#b5e1ac',
    '#f48787',
    '#ff9896',
    '#9467bd',
    '#c5b0d5',
    '#e4c0e1',
    '#c49c94',
    '#e377c2',
    '#dcd0d9',
    '#7f7f7f',
    '#c7c7c7',
    '#bcbd22',
    '#dbdb8d',
    '#17becf',
    '#a5d8d7',
];

function getCustomColor(index) {
    const colorScheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? CUSTOM_COLORS_DARK
        : CUSTOM_COLORS_BRIGHT;

    return colorScheme[index % colorScheme.length];
}

patch(GraphRenderer.prototype, {
    getLineChartData() {
        const data = super.getLineChartData();

        data.datasets.forEach((dataset, index) => {
            const color = getCustomColor(index);
            dataset.borderColor = color;
            dataset.pointBackgroundColor = color;
            dataset.backgroundColor = color + '10';
            dataset.fill = true;
        });

        return data;
    },

    getBarChartData() {
        const data = super.getBarChartData();

        data.datasets.forEach((dataset, index) => {
            dataset.backgroundColor = getCustomColor(index);
        });

        return data;
    },

    getPieChartData() {
        const data = super.getPieChartData();
        const colors = data.labels.map((_, index) => getCustomColor(index));

        data.datasets.forEach((dataset) => {
            dataset.backgroundColor = colors;
        });

        return data;
    },
});
