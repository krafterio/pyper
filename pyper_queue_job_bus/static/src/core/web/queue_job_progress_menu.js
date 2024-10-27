/* @odoo-module */

import {Component, onMounted, useState} from '@odoo/owl';

import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';

export class ProgressMenu extends Component {
    static template = 'pyper_queue_job_bus.ProgressMenu';

    static props = {};

    setup() {
        this.queueJobService = useState(useService('queue_job'));
        this.actionService = useService('action');

        onMounted(() => {
            this.env.bus.trigger('QUEUE-JOB:UPDATED');
        });
    }

    get counter() {
        return this.queueJobService.counter;
    }

    get displayIcon() {
        return this.counter > 0;
    }

    onClick() {
        this.actionService.doAction('pyper_queue_job.pyper_queue_job_action_simple').then();
    }
}

registry
    .category('systray')
    .add('pyper_queue_job_bus.progress_menu', {Component: ProgressMenu}, {sequence: 10000})
;
