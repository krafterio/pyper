/** @odoo-module **/

import {Component, onWillUnmount, useEffect} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {standardWidgetProps} from '@web/views/widgets/standard_widget_props';

export class OpenAiStream extends Component {
    static template = 'pyper_openai_stream.OpenAiStream';

    static props = {
        ...standardWidgetProps,
        model: {
            type: String,
            optional: true,
        },
        systemMessageField: {
            type: String,
            optional: true,
        },
        userMessageField: {
            type: String,
        },
        targetField: {
            type: String,
        },
        endMessageField: {
            type: String,
            optional: true,
        },
    };

    setup() {
        this.rpc = useService('rpc');
        this.eventSource = null;

        useEffect(this._changeValues.bind(this), this._getComputeDependencies.bind(this));

        onWillUnmount(() => {
            if (this.eventSource) {
                this.eventSource.close();
            }
        });
    }

    _getComputeDependencies() {
        const deps = [
            this.props.record?.data[this.props.model],
            this.props.record?.data[this.props.userMessageField],
        ];

        if (this.props.systemMessageField && this.props.record?.data[this.props.systemMessageField]) {
            deps.push(this.props.record?.data[this.props.systemMessageField]);
        }

        return deps;
    }

    _changeValues() {
        this._initializeStream().then();
    }

    async _initializeStream() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }

        const systemMessage = this.props.record?.data[this.props.systemMessageField] || undefined;
        const userMessage = this.props.record?.data[this.props.userMessageField] || undefined;

        if (!userMessage || 0 === userMessage.length) {
            return;
        }

        const res = await this.rpc('/openai/stream', {
            'model': this.props.model,
            'system_message': systemMessage,
            'user_message': userMessage,
        });

        this.props.record.data[this.props.targetField] = '';
        this.eventSource = new EventSource(`/openai/stream/${res.identifier}`);

        this.eventSource.addEventListener('message', async (event) => {
            this.props.record.data[this.props.targetField] += event.data;
        });

        this.eventSource.addEventListener('end', () => {
            this.eventSource.close();
            this.eventSource = null;

            if (this.props.endMessageField && this.props.record?.data[this.props.endMessageField]) {
                this.props.record.data[this.props.targetField] += this.props.record?.data[this.props.endMessageField];
            }
        });

        this.eventSource.addEventListener('error', (e) => {
            this.eventSource.close();
            this.eventSource = null;

            throw e;
        });
    }
}
