/** @odoo-module **/

import {Component, onWillStart, onWillUpdateProps, onMounted, onWillUnmount, useState, useSubEnv} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {makeContext} from '@web/core/context';
import {View} from '@web/views/view';
import {rpc} from '@web/core/network/rpc';
import {user} from '@web/core/user';

export class DashboardAction extends Component {
    static template = 'pyper_dashboard.DashboardAction';

    static components = {
        View,
    };

    static props = {
        type: {
            type: String,
            optional: true,
        },
        title: {
            type: String,
            optional: true,
        },
        icon: {
            type: String,
            optional: true,
        },
        actionId: {
            type: [Number, String],
            optional: true,
        },
        resModel: {
            type: String,
            optional: true,
        },
        viewMode: {
            type: String,
            optional: true,
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
        height: {
            type: String,
            optional: true,
        },
        minHeight: {
            type: String,
            optional: true,
        },
        maxHeight: {
            type: String,
            optional: true,
        },
    };

    static defaultProps = {
        context: {},
        domain: [],
    }

    static cache = {};

    setup() {
        this.actionService = useService('action');
        this.orm = useService('orm');
        this.formViewId = false;
        this.isValid = true;
        this.isKpi = false;
        this.kpiData = useState({
            subtitle: '',
            measureField: '__count',
            measureMethod: 'count',
            value: null,
        });
        this.viewProps = useState({});
        this.dashboardState = {skipAnimation: false};

        useSubEnv({dashboardState: this.dashboardState});

        this._onDashboardRefresh = () => this._refresh();

        onWillStart(async () => {
            await this._loadAction(this.props);
        });

        onWillUpdateProps(async (nextProps) => {
            await this._onPropsUpdate(nextProps);
        });

        onMounted(() => {
            this.env.bus.addEventListener('dashboard-refresh', this._onDashboardRefresh);
        });

        onWillUnmount(() => {
            this.env.bus.removeEventListener('dashboard-refresh', this._onDashboardRefresh);
        });
    }

    get showView() {
        return this.isValid && !this.isKpi;
    }

    get formattedKpiValue() {
        if (this.kpiData.value === null || this.kpiData.value === undefined) {
            return '---';
        }

        return this.kpiData.value.toLocaleString();
    }

    async _loadAction(props) {
        if (props.type === 'kpi') {
            this.isKpi = true;
            await this._loadKpiData(props);

            return;
        }

        if (props.actionId) {
            // Mode: existing action
            let result = DashboardAction.cache[props.actionId];

            if (!result) {
                result = await rpc('/web/action/load', {action_id: props.actionId});
                DashboardAction.cache[props.actionId] = result;
            }

            if (!result) {
                this.isValid = false;

                return;
            }

            const viewMode = props.viewMode || result.views[0][1];
            const formView = result.views.find((v) => v[1] === 'form');

            if (formView) {
                this.formViewId = formView[0];
            }

            Object.assign(this.viewProps, {
                resModel: result.res_model,
                type: viewMode,
                display: {
                    controlPanel: false,
                    searchPanel: false,
                },
                selectRecord: (resId) => this.selectRecord(result.res_model, resId),
            });

            const view = result.views.find((v) => v[1] === viewMode);

            if (view) {
                this.viewProps.viewId = view[0];
            }

            const searchView = result.views.find((v) => v[1] === 'search');

            this.viewProps.views = [
                [this.viewProps.viewId || false, viewMode],
                [(searchView && searchView[0]) || false, 'search'],
            ];
        } else if (props.resModel) {
            // Mode: direct view (without existing action)
            const viewMode = props.viewMode;

            Object.assign(this.viewProps, {
                resModel: props.resModel,
                type: viewMode,
                display: {
                    controlPanel: false,
                    searchPanel: false,
                },
                views: [[false, viewMode], [false, 'search']],
            });
        } else {
            this.isValid = false;

            return;
        }

        const viewMode = this.viewProps.type;

        if (props.context) {
            this.viewProps.context = makeContext([
                props.context,
                {lang: user.context.lang},
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
                    this.viewProps.comparison = comparison;
                }
            }
        }

        if (props.domain) {
            this.viewProps.domain = props.domain;
        }

        this.viewProps.context = {
            ...this.viewProps.context,
            create: false,
            edit: false,
            delete: false,
        };

        if (viewMode === 'list') {
            this.viewProps.allowSelectors = false;
        }
    }

    async _loadKpiData(props) {
        const ctx = props.context || {};
        this.kpiData.subtitle = ctx.kpi_subtitle || '';
        this.kpiData.measureField = ctx.kpi_measure_field || '__count';
        this.kpiData.measureMethod = ctx.kpi_measure_method || 'count';
        this.kpiData.value = null;

        if (!props.resModel) {
            this.isValid = false;

            return;
        }

        try {
            const domain = props.domain || [];
            const method = this.kpiData.measureMethod;
            const field = this.kpiData.measureField;
            const hasField = method !== 'count' && field && field !== '__count';
            const fields = hasField ? [`${field}:${method}`] : [];

            const result = await this.orm.call(
                props.resModel,
                'read_group',
                [domain, fields, []],
            );

            if (result && result.length > 0) {
                if (hasField) {
                    this.kpiData.value = result[0][field] ?? 0;
                } else {
                    this.kpiData.value = result[0].__count || 0;
                }
            } else {
                this.kpiData.value = 0;
            }
        } catch {
            this.kpiData.value = null;
            this.isValid = false;
        }
    }

    async _onPropsUpdate(nextProps) {
        if (this.isKpi) {
            const domainChanged = JSON.stringify(nextProps.domain) !== JSON.stringify(this.props.domain);

            if (domainChanged) {
                await this._loadKpiData(nextProps);
            }
        } else if (this.isValid) {
            if (nextProps.domain) {
                this.viewProps.domain = nextProps.domain;
            }
        }
    }

    async _refresh() {
        this.dashboardState.skipAnimation = true;

        if (this.isKpi) {
            await this._loadKpiData(this.props);
            this.dashboardState.skipAnimation = false;
        } else if (this.isValid) {
            // Force View to detect a change by creating a new domain reference
            this.viewProps.domain = [...(this.props.domain || [])];
        }
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
