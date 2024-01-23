/** @odoo-module */

import {registry} from '@web/core/registry';
import {ProgressCircular, progressCircular} from '@pyper/views/fields/progress_circular/progress_circular_field';

export class ProgressCircularKendama extends ProgressCircular {
    static template = 'smashr.ProgressCircularKendama';

    static defaultProps = {
        ...super.defaultProps,
        min: 0,
        max: 9,
        displayValue: true,
        hideEmpty: true,
    };

    get classes() {
        const classes = super.classes;

        delete classes['progress-circular--' + this.props.color];
        classes['progress-circular--' + this.overlayStrokeColor] = true;

        return classes;
    }

    get overlayStrokeColor() {
        if (this.value > 0 && this.value <= 3) {
            return 'primary';
        }

        if (this.value > 3 && this.value <= 6) {
            return 'warning';
        }

        if (this.value > 6 && this.value <= 9) {
            return 'danger';
        }
    }
}

export const progressCircularKendama = {
    ...progressCircular,
    component: ProgressCircularKendama,
    displayName: 'Progress Circular Kendama',
};

registry.category('fields').add('progress_circular_kendama', progressCircularKendama);
