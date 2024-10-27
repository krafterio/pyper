/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {registry} from '@web/core/registry';

export class QueueJobState {
    constructor(envBus, busService, orm, user) {
        this.envBus = envBus;
        this.bus = busService;
        this.orm = orm;
        this.user = user;
    }

    setup() {
        this.state = reactive({
            counter: 0,
        });

        this.envBus.addEventListener('QUEUE-JOB:UPDATED', this._onUpdated.bind(this));

        this.bus.subscribe('queue_job_updated', this._onUpdated.bind(this));
        this.bus.start();
    }

    get counter() {
        return this.state.counter;
    }

    async _onUpdated() {
        this.state.counter = await this.orm.searchCount('pyper.queue.job', [
            ['user_id', '=', this.user.userId],
            ['state', 'not in', ['done', 'cancelled']],
        ]);
    }
}

export const queueJobService = {
    dependencies: ['bus_service', 'orm', 'user'],
    start(env, {bus_service, orm, user}) {
        const queueJobState = reactive(new QueueJobState(env.bus, bus_service, orm, user));
        queueJobState.setup();

        return queueJobState;
    },
};

registry.category('services').add('queue_job', queueJobService);
