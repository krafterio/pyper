/** @odoo-module **/

import {Component, onWillStart} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {makeContext} from '@web/core/context';
import {View} from '@web/views/view';

export class DashboardAction extends Component {
    static template = 'pyper_dashboard.DashboardAction';

    static components = {
        View,
    };

    static props = {
        title: {
            type: String,
            optional: true,
        },
        actionId: {
            type: [Number, String],
        },
        viewMode: {
            type: String,
        },
        context: {
            type: Object,
            optional: true,
        },
        domain: {
            type: Array,
            optional: true,
        },
        attr: {
            type: Object,
            optional: true,
        },
    };

    static defaultProps = {
        context: {},
        domain: [],
    }

    static cache = {};

    setup() {
        const rpc = useService('rpc');
        const userService = useService('user');
        this.actionService = useService('action');
        this.formViewId = false;
        this.isValid = true;
        this.viewProps = {};

        onWillStart(async () => {
            let result = DashboardAction.cache[this.props.actionId];

            if (!result) {
                result = await rpc('/web/action/load', {action_id: this.props.actionId});
                DashboardAction.cache[this.props.actionId] = result;
            }

            if (!result) {
                this.isValid = false;

                return;
            }

            const viewMode = this.props.viewMode || result.views[0][1];
            const formView = result.views.find((v) => v[1] === 'form');

            if (formView) {
                this.formViewId = formView[0];
            }

            this.viewProps = {
                resModel: result.res_model,
                type: viewMode,
                display: {
                    controlPanel: false,
                    searchPanel: false,
                },
                selectRecord: (resId) => this.selectRecord(result.res_model, resId),
            };

            const view = result.views.find((v) => v[1] === viewMode);

            if (view) {
                this.viewProps.viewId = view[0];
            }

            const searchView = result.views.find((v) => v[1] === 'search');

            this.viewProps.views = [
                [this.viewProps.viewId || false, viewMode],
                [(searchView && searchView[0]) || false, 'search'],
            ];

            if (this.props.context) {
                this.viewProps.context = makeContext([
                    this.props.context,
                    {lang: userService.context.lang},
                ]);

                if ('group_by' in this.viewProps.context) {
                    const groupBy = this.viewProps.context.group_by;
                    this.viewProps.groupBy = typeof groupBy === 'string' ? [groupBy] : groupBy;
                }

                if ('order_by' in this.viewProps.context) {
                    const orderBy = this.viewProps.context.order_by;
                    this.viewProps.orderBy = typeof orderBy === 'string' ? [orderBy] : orderBy;
                }

                if ('limit' in this.viewProps.context && ['list', 'kanban'].includes(viewMode)) {
                    this.viewProps.limit = this.viewProps.context.limit;
                }

                if ('comparison' in this.viewProps.context) {
                    const comparison = this.viewProps.context.comparison;

                    if (
                        comparison !== null
                        && typeof comparison === 'object'
                        && 'domains' in comparison
                        && 'fieldName' in comparison
                    ) {
                        // Some comparison object with the wrong form might have been stored in db.
                        // This is why we make the checks on the keys domains and fieldName
                        this.viewProps.comparison = comparison;
                    }
                }
            }

            if (this.props.domain) {
                this.viewProps.domain = this.props.domain;
            }

            if (viewMode === 'list') {
                this.viewProps.allowSelectors = false;
            }
        });
    }

    get showView() {
        return this.isValid;
    }

    selectRecord(resModel, resId) {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: resModel,
            views: [[this.formViewId, 'form']],
            res_id: resId,
        });
    }
}
