/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {user} from '@web/core/user';

export class QueueJobState {
    constructor(busService, orm) {
        this.bus = busService;
        this.orm = orm;
    }

    setup() {
        this.state = reactive({
            counter: 0,
        });

        this.bus.subscribe('queue_job_updated', this._onUpdated.bind(this));
        this._onUpdated().then();
    }

    get counter() {
        return this.state.counter;
    }

    async _onUpdated() {
        this.state.counter = await this.orm.searchCount('pyper.queue.job', [
            ['user_id', '=', user.userId],
            ['state', 'not in', ['done', 'cancelled']],
        ]);
    }
}

export const queueJobService = {
    dependencies: ['bus_service', 'orm'],
    start(env, {bus_service, orm}) {
        const queueJobState = reactive(new QueueJobState(bus_service, orm));
        queueJobState.setup();

        return queueJobState;
    },
};

registry.category('services').add('queue_job', queueJobService);
