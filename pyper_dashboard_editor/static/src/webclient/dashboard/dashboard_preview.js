/** @odoo-module **/

import {captureSearchModelState} from './dashboard_search_model_utils';
import {DASHBOARD_PREVIEW_MODE, GRAPH_CONTEXT_KEYS, PAGER_PROPS_REF} from './dashboard_preview_constants';
import {Component, onMounted, onWillStart, useSubEnv} from '@odoo/owl';
import {patch} from '@web/core/utils/patch';
import {View} from '@web/views/view';
import {ControlPanel} from '@web/search/control_panel/control_panel';
import {WithSearch} from '@web/search/with_search/with_search';
import {rpc} from '@web/core/network/rpc';

const SEARCH_MODEL_REF = Symbol('previewSearchModelRef');
const PREVIEW_INTERNAL_CONTEXT_KEYS = ['create', 'edit', 'delete'];

patch(WithSearch.prototype, {
    setup() {
        super.setup();

        const ref = this.env[SEARCH_MODEL_REF];

        if (ref) {
            ref.current = this.searchModel;
        }
    },
});

patch(ControlPanel.prototype, {
    setup() {
        super.setup();

        const ref = this.env[PAGER_PROPS_REF];

        if (ref) {
            ref.current = this.env.config.pagerProps;
        }
    },
});

export class DashboardPreview extends Component {
    static template = 'pyper_dashboard_editor.DashboardPreview';

    static components = {
        View,
    };

    static props = {
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
        },
        context: {
            type: Object,
            optional: true,
        },
        domain: {
            type: Array,
            optional: true,
        },
        onReady: {
            type: Function,
            optional: true,
        },
    };

    setup() {
        this.isValid = true;
        this.viewProps = {};
        this.searchModelRef = {current: null};
        this.pagerPropsRef = {current: null};

        useSubEnv({
            [SEARCH_MODEL_REF]: this.searchModelRef,
            [DASHBOARD_PREVIEW_MODE]: true,
            [PAGER_PROPS_REF]: this.pagerPropsRef,
        });

        onWillStart(async () => {
            if (this.props.actionId) {
                const result = await rpc('/web/action/load', {action_id: this.props.actionId});

                if (!result) {
                    this.isValid = false;

                    return;
                }

                const viewMode = this.props.viewMode || result.views[0][1];
                const view = result.views.find((v) => v[1] === viewMode);
                const searchView = result.views.find((v) => v[1] === 'search');

                this.viewProps = {
                    resModel: result.res_model,
                    type: viewMode,
                    display: {
                        controlPanel: {},
                        searchPanel: false,
                    },
                    viewId: view ? view[0] : false,
                    views: [
                        [view ? view[0] : false, viewMode],
                        [(searchView && searchView[0]) || false, 'search'],
                    ],
                };
            } else if (this.props.resModel) {
                this.viewProps = {
                    resModel: this.props.resModel,
                    type: this.props.viewMode,
                    display: {
                        controlPanel: {},
                        searchPanel: false,
                    },
                    views: [[false, this.props.viewMode], [false, 'search']],
                };
            } else {
                this.isValid = false;

                return;
            }

            if (this.props.context && Object.keys(this.props.context).length) {
                // Create a plain copy to bypass OWL reactive proxy issues
                const plainContext = {};

                for (const [key, value] of Object.entries(this.props.context)) {
                    if (key !== 'toString') {
                        plainContext[key] = value;
                    }
                }

                if (Object.keys(plainContext).length) {
                    this.viewProps.context = plainContext;

                    if ('group_by' in plainContext) {
                        const groupBy = plainContext.group_by;
                        this.viewProps.groupBy = typeof groupBy === 'string' ? [groupBy] : groupBy;
                    }

                    if ('order_by' in plainContext) {
                        const orderBy = plainContext.order_by;
                        this.viewProps.orderBy = typeof orderBy === 'string' ? [orderBy] : orderBy;
                    }

                    if ('limit' in plainContext && ['list', 'kanban'].includes(this.viewProps.type)) {
                        this.viewProps.limit = plainContext.limit;
                    }
                }
            }

            if (this.props.domain?.length) {
                this.viewProps.domain = this.props.domain;
            }

            this.viewProps.context = {
                ...this.viewProps.context,
                create: false,
                edit: false,
                delete: false,
            };

            if (this.viewProps.type === 'list') {
                this.viewProps.allowSelectors = false;
            }
        });

        onMounted(() => {
            const searchModel = this.searchModelRef.current;

            if (searchModel) {
                searchModel.blockNotification = true;

                // Remove graph settings from globalContext so they don't override
                // interactive changes (e.g., changing measure would reset graph_mode)
                if (searchModel.globalContext) {
                    for (const key of GRAPH_CONTEXT_KEYS) {
                        delete searchModel.globalContext[key];
                    }

                    searchModel._context = null;
                }

                // Activate group_by items as visible facets in the search bar
                // (globalGroupBy applies silently without showing facets)
                this._activateGroupByFacets(searchModel);

                searchModel.blockNotification = false;
                searchModel._notify();
            }

            this.props.onReady?.(() => this.getState());
        });
    }

    getState() {
        const searchModel = this.searchModelRef.current;

        if (!searchModel) {
            return {};
        }

        const state = captureSearchModelState(searchModel);

        // Capture limit from pagerProps (searchModel.env doesn't have access to
        // controller's pagerProps — it's set via useSubEnv which only affects children)
        const pagerLimit = this.pagerPropsRef.current?.limit;

        if (pagerLimit && ['list', 'kanban'].includes(this.viewProps.type)) {
            state.context.limit = pagerLimit;
        }

        // Remove internal preview context keys that should not be saved
        for (const key of PREVIEW_INTERNAL_CONTEXT_KEYS) {
            delete state.context[key];
        }

        // Clean up empty arrays
        if (Array.isArray(state.context.order_by) && !state.context.order_by.length) {
            delete state.context.order_by;
        }

        if (Array.isArray(state.context.group_by) && !state.context.group_by.length) {
            delete state.context.group_by;
        }

        return state;
    }

    _activateGroupByFacets(searchModel) {
        const groupBy = this.props.context?.group_by;

        if (!groupBy) {
            return;
        }

        const fields = Array.isArray(groupBy) ? groupBy : [groupBy];

        for (const fieldSpec of fields) {
            const [fieldName, interval] = fieldSpec.split(':');

            // Check if a matching groupBy item already exists in the search view
            const existing = searchModel.getSearchItems(
                (item) => item.type === 'groupBy' && item.fieldName === fieldName
            );

            if (existing.length) {
                searchModel.toggleSearchItem(existing[0].id);
            } else if (fieldName in searchModel.searchViewFields) {
                searchModel.createNewGroupBy(fieldName, {interval});
            }
        }

        // Clear globalGroupBy since items are now active as facets
        searchModel.globalGroupBy = [];
    }
}
