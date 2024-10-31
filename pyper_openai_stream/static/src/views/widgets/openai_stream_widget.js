/** @odoo-module **/

import {registry} from '@web/core/registry';
import {OpenAiStream} from './openai_stream';

export const openAiStreamWidget = {
    component: OpenAiStream,
    extractProps: ({attrs}) => {
        return {
            model: attrs.model || undefined,
            systemMessageField: attrs['system_message_field'] || undefined,
            userMessageField: attrs['user_message_field'] || undefined,
            targetField: attrs['target_field'] || undefined,
        };
    },
};

registry.category('view_widgets').add('openai_stream', openAiStreamWidget);
