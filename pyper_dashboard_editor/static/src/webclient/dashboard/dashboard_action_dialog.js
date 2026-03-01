/** @odoo-module **/

import {dashboardActionTypeRegistry} from './dashboard_action_type_registry';
import {DashboardKpiPreview} from './dashboard_kpi_preview';
import {DashboardPreview} from './dashboard_preview';
import {onWillStart, useState} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {ModelSelector} from '@web/core/model_selector/model_selector';
import {ModelFieldSelector} from '@web/core/model_field_selector/model_field_selector';
import {RecordSelector} from '@web/core/record_selectors/record_selector';
import {SelectMenu} from '@web/core/select_menu/select_menu';
import {useService} from '@web/core/utils/hooks';
import {rpc} from '@web/core/network/rpc';
import {DashboardDialogBase, useControlledInput} from './dashboard_dialog';

const EXCLUDED_VIEW_TYPES = ['form', 'search', 'qweb', 'activity'];

export class DashboardActionDialog extends DashboardDialogBase {
    static template = 'pyper_dashboard_editor.DashboardActionDialog';

    static components = {
        ...DashboardDialogBase.components,
        ModelSelector,
        ModelFieldSelector,
        RecordSelector,
        SelectMenu,
        DashboardPreview,
        DashboardKpiPreview,
    };

    static props = {
        ...DashboardDialogBase.props,
        type: {
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
        title: {
            type: String,
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
        filterField: {
            type: String,
            optional: true,
        },
        filterFieldType: {
            type: String,
            optional: true,
        },
        icon: {
            type: String,
            optional: true,
        },
    };

    static defaultProps = {
        ...DashboardDialogBase.defaultProps,
        dialogTitle: _t('Action'),
    }

    setup() {
        super.setup();

        this.orm = useService('orm');
        this.title = useControlledInput(this.props.title, value => !!value || !value);
        this.icon = useControlledInput(this.props.icon, () => true);
        this.height = useControlledInput(this.props.height, value => !value || /^\d+(px|vh)$/.test(value));
        this.minHeight = useControlledInput(this.props.minHeight, value => !value || /^\d+(px|vh)$/.test(value));
        this.maxHeight = useControlledInput(this.props.maxHeight, value => !value || /^\d+(px|vh)$/.test(value));

        this.actionTypes = [];
        this.allViewTypes = [];
        this._getPreviewState = null;
        Object.defineProperty(this, 'getPreviewState', {
            get: () => this._getPreviewState,
            set: (val) => { this._getPreviewState = val; },
            configurable: true,
        });

        this.state = useState({
            type: this.props.type || 'action',
            viewTypes: [],
            selectedActionId: this.props.actionId || false,
            modelName: this.props.resModel || '',
            modelLabel: '',
            viewMode: this.props.viewMode || '',
            showPreview: false,
            previewKey: 0,
            filterField: this.props.filterField || '',
            filterFieldType: this.props.filterFieldType || '',
            errors: {
                model: false,
                action: false,
            },
        });

        onWillStart(async () => {
            // Load action types from registry
            const entries = dashboardActionTypeRegistry.getEntries();
            this.actionTypes = entries
                .map(([key, val]) => ({key, ...val}))
                .sort((a, b) => (a.sequence || 0) - (b.sequence || 0));

            // Load available view types
            const viewTypeFields = await this.orm.call('ir.ui.view', 'fields_get', [['type']]);

            if (viewTypeFields?.type?.selection) {
                this.allViewTypes = viewTypeFields.type.selection
                    .filter(([key]) => !EXCLUDED_VIEW_TYPES.includes(key));
                this.state.viewTypes = [...this.allViewTypes];
            }

            // Pre-fill for edit mode
            if (this.props.actionId) {
                const result = await rpc('/web/action/load', {action_id: this.props.actionId});

                if (result) {
                    this.state.modelName = result.res_model;
                    this.state.modelLabel = await this._fetchModelLabel(result.res_model);
                    this._filterViewTypes(result.views);
                }

                this.state.showPreview = !!this.state.viewMode;
            } else if (this.props.resModel) {
                this.state.modelLabel = await this._fetchModelLabel(this.props.resModel);
                this._setDefaultViewMode();
                this.state.showPreview = this.isKpiType || !!this.state.viewMode;
            } else {
                this._setDefaultViewMode();
            }
        });
    }

    get dialogSize() {
        return 'xl';
    }

    get actionTypeChoices() {
        return this.actionTypes.map((at) => ({value: at.key, label: at.label}));
    }

    get viewTypeChoices() {
        return this.state.viewTypes.map(([value, label]) => ({value, label}));
    }

    get isKpiType() {
        return this.state.type === 'kpi';
    }

    get actionDomain() {
        if (this.state.modelName) {
            return [['res_model', '=', this.state.modelName]];
        }

        return [];
    }

    get previewProps() {
        // Create a plain copy of the context to bypass OWL reactive proxy issues
        let context;

        if (this.props.context) {
            context = {};

            for (const [key, value] of Object.entries(this.props.context)) {
                if (key !== 'toString') {
                    context[key] = value;
                }
            }

            if (!Object.keys(context).length) {
                context = undefined;
            }
        }

        if (this.isKpiType) {
            const props = {
                resModel: this.state.modelName,
                context,
                onReady: (getStateFn) => this.onPreviewReady(getStateFn),
            };

            if (this.props.domain?.length) {
                props.domain = this.props.domain;
            }

            return props;
        }

        const props = {
            viewMode: this.state.viewMode,
            context,
            onReady: (getStateFn) => this.onPreviewReady(getStateFn),
        };

        if (this.props.domain?.length) {
            props.domain = this.props.domain;
        }

        if (this.state.type === 'action' && this.state.selectedActionId) {
            props.actionId = this.state.selectedActionId;
        } else if (this.state.modelName) {
            props.resModel = this.state.modelName;
        }

        return props;
    }

    get filterFieldFilter() {
        return (fieldDef) => ['date', 'datetime'].includes(fieldDef.type);
    }

    get formData() {
        const previewState = this.getPreviewState?.() || {};
        const actionId = this.state.type === 'action' ? this.state.selectedActionId : undefined;

        return {
            type: actionId ? 'action' : this.state.type,
            actionId: actionId || undefined,
            resModel: !actionId ? this.state.modelName : undefined,
            title: this.title.input.value || undefined,
            icon: this.icon.input.value || undefined,
            viewMode: this.isKpiType ? undefined : this.state.viewMode,
            context: previewState.context || {},
            domain: previewState.domain || [],
            height: this.isKpiType ? undefined : (this.height.input.value || undefined),
            minHeight: this.isKpiType ? undefined : (this.minHeight.input.value || undefined),
            maxHeight: this.isKpiType ? undefined : (this.maxHeight.input.value || undefined),
            filterField: this.state.filterField || undefined,
            filterFieldType: this.state.filterFieldType || undefined,
        };
    }

    isFormValid() {
        let valid = true;

        this.state.errors.model = !this.state.modelName;
        this.state.errors.action = this.state.type === 'action' && !this.state.selectedActionId;

        if (this.state.errors.model || this.state.errors.action) {
            valid = false;
        }

        valid = this.title.isValid() && valid;
        valid = this.height.isValid() && valid;
        valid = this.minHeight.isValid() && valid;
        valid = this.maxHeight.isValid() && valid;

        return valid;
    }

    onPreviewReady(getStateFn) {
        this.getPreviewState = getStateFn;
    }

    onTypeChanged(value) {
        this.state.type = value;
        this.state.selectedActionId = false;

        if (value !== 'action' && value !== 'kpi') {
            this.state.viewTypes = [...this.allViewTypes];
            this._setDefaultViewMode();
        }

        this._updatePreview();
    }

    onModelSelected({technical, label}) {
        this.state.modelName = technical;
        this.state.modelLabel = label;
        this.state.selectedActionId = false;
        this.state.errors.model = false;
        this.state.filterField = '';
        this.state.filterFieldType = '';
        this.state.viewTypes = [...this.allViewTypes];
        this._setDefaultViewMode();
        this._updatePreview();
    }

    onFilterFieldUpdate(path, fieldInfo) {
        this.state.filterField = path || '';
        this.state.filterFieldType = fieldInfo?.fieldDef?.type || '';
    }

    async onActionSelected(resId) {
        this.state.selectedActionId = resId || false;
        this.state.errors.action = false;

        if (resId) {
            const result = await rpc('/web/action/load', {action_id: resId});

            if (result?.views) {
                this._filterViewTypes(result.views);
            }
        } else {
            this.state.viewTypes = [...this.allViewTypes];
            this._setDefaultViewMode();
        }

        this._updatePreview();
    }

    onViewModeChanged(value) {
        this.state.viewMode = value;
        this._updatePreview();
    }

    _filterViewTypes(views) {
        const actionViewTypes = views
            .map((v) => v[1])
            .filter((vt) => !EXCLUDED_VIEW_TYPES.includes(vt));
        this.state.viewTypes = this.allViewTypes.filter(
            ([key]) => actionViewTypes.includes(key)
        );
        this._setDefaultViewMode();
    }

    async _fetchModelLabel(modelName) {
        const result = await this.orm.call('ir.model', 'display_name_for', [[modelName]]);

        return result[0]?.display_name || modelName;
    }

    _setDefaultViewMode() {
        if (!this.state.viewMode || !this.state.viewTypes.some(([key]) => key === this.state.viewMode)) {
            this.state.viewMode = this.state.viewTypes.length > 0 ? this.state.viewTypes[0][0] : '';
        }
    }

    _updatePreview() {
        this.getPreviewState = null;
        const hasSource = this.state.type === 'action'
            ? !!this.state.selectedActionId
            : !!this.state.modelName;

        if (this.isKpiType) {
            this.state.showPreview = hasSource;
        } else {
            this.state.showPreview = hasSource && !!this.state.viewMode;
        }

        if (this.state.showPreview) {
            this.state.previewKey++;
        }
    }
}
