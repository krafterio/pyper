/** @odoo-module **/

import {Component} from '@odoo/owl';
import {url} from '@web/core/utils/urls';
import {Field} from '@web/views/fields/field';
import {fileTypeMagicWordMap, imageCacheKey} from '@web/views/fields/image/image_field';
import {Widget} from '@web/views/widgets/widget';


export const isBinSize = function(value) {
    return /^\d+(\.\d*)? [^0-9]+$/.test(value);
};

export const getImageSrcFromItemInfo = function(record, model, field, idOrIds, placeholder) {
    const id = (Array.isArray(idOrIds) ? idOrIds[0] : idOrIds) || null;
    const isCurrentRecord = record.resModel === model && (record.resId === id || (!record.resId && !id));
    const fieldVal = record.data[field];

    if (isCurrentRecord && fieldVal && !isBinSize(fieldVal)) {
        // Use magic-word technique for detecting image type
        const type = fileTypeMagicWordMap[fieldVal[0]];

        return `data:image/${type};base64,${fieldVal}`;
    } else if (placeholder && (!model || !field || !id || !fieldVal)) {
        // Placeholder if either the model, field, id or value is missing or null.
        return placeholder;
    } else {
        // Else: fetches the image related to the given id.
        const params = {
            model,
            field,
            id,
        };

        if (isCurrentRecord) {
            params.unique = imageCacheKey(record.data.write_date);
        }

        return url('/web/image', params);
    }
}

export class TimelineRecord extends Component {
    static template = 'pyper_timeline.TimelineRecord';

    static components = {
        Field,
        Widget,
    };

    static props = [
        'archInfo',
        'Compiler?',
        'readonly?',
        'label?',
        'record',
        'templateName?',
        'templates',
    ];

    get JSON() {
        return JSON;
    }

    get templateName() {
        return this.props.templateName || 'itemTemplate';
    }

    get renderingContext() {
        return {
            JSON,
            timeline_image: (...args) => getImageSrcFromItemInfo(this.props.record, ...args),
            luxon,
            label: this.props.label,
            record: this.props.record,
            user_context: this.constructor.env.services.user.context,
            __comp__: Object.assign(Object.create(this), {this: this}),
        }
    }
}
