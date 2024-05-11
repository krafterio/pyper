/** @odoo-module **/

import {TimelineRecord} from './timeline_record';

export class TimelinePopover extends TimelineRecord {
    static template = 'pyper_pipeline.TimelinePopover';

    static props = {
        ...super.props,
        ...{
            close: {
                type: Function,
                optional: false,
            },
            button: {
                type: Object,
                optional: true,
            },
        },
    };

    get templateName() {
        return this.props.templateName;
    }

    get computedTemplate() {
        if (!this.templateName) {
            return 'pyper_pipeline.TimelinePopover.default';
        }

        return super.computedTemplate;
    }

    onClick() {
        this.props.button.onClick();
        this.props.close();
    }
}
