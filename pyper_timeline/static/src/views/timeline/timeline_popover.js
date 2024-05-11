/** @odoo-module **/

import {Component} from '@odoo/owl';
import {getImageSrcFromItemInfo} from './timeline_record';
import {Field} from '@web/views/fields/field';
import {Widget} from '@web/views/widgets/widget';

export class TimelinePopover extends Component {
    static template = 'pyper_pipeline.TimelinePopover';

    static components = {
        Field,
        Widget,
    };

    static props = {
        archInfo: {
            type: Object,
            optional: false,
        },
        Compiler: {
            type: Function,
            optional: true,
        },
        title: {
            type: String,
            optional: false,
        },
        record: {
            type: Object,
            optional: false,
        },
        template: {
            type: String,
            optional: true,
        },
        context: {
            type: Object,
            optional: false,
        },
        close: {
            type: Function,
            optional: false,
        },
        button: {
            type: Object,
            optional: true,
        },
    };

    static defaultProps = {
        template: 'pyper_pipeline.TimelinePopover.default',
    };

    get renderingContext() {
        return {
            ...(this.props.context || {}),
            JSON,
            timeline_image: (...args) => getImageSrcFromItemInfo(this.props.record, ...args),
            luxon,
            title: this.props.title,
            record: this.props.record,
            user_context: this.constructor.env.services.user.context,
            __comp__: Object.assign(Object.create(this), {this: this}),
            ...this.props.context,
        };
    }

    onClick() {
        this.props.button.onClick();
        this.props.close();
    }
}
