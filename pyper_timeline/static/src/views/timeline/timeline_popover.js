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
            editButton: {
                type: Object,
                optional: true,
            },
            deleteButton: {
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

    onEditClick() {
        this.props.editButton.onClick();
        this.props.close();
    }

    onDeleteClick() {
        this.props.deleteButton.onClick();
        this.props.close();
    }
}
