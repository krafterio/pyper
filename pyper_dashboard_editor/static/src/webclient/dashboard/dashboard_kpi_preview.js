/** @odoo-module **/

import {Component, onMounted, onWillStart, useState} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {Domain} from '@web/core/domain';
import {DomainSelector} from '@web/core/domain_selector/domain_selector';
import {ModelFieldSelector} from '@web/core/model_field_selector/model_field_selector';
import {SelectMenu} from '@web/core/select_menu/select_menu';
import {useService} from '@web/core/utils/hooks';

export class DashboardKpiPreview extends Component {
    static template = 'pyper_dashboard_editor.DashboardKpiPreview';

    static components = {
        DomainSelector,
        ModelFieldSelector,
        SelectMenu,
    };

    static props = {
        resModel: {
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
        this.orm = useService('orm');

        const ctx = this.props.context || {};
        const domainArray = this.props.domain || [];
        this.state = useState({
            subtitle: ctx.kpi_subtitle || '',
            measureField: ctx.kpi_measure_field || '__count',
            measureMethod: ctx.kpi_measure_method || 'count',
            domainStr: domainArray.length ? new Domain(domainArray).toString() : '[]',
            kpiValue: null,
            isLoading: true,
        });

        onWillStart(async () => {
            await this._fetchKpiValue();
        });

        onMounted(() => {
            this.props.onReady?.(() => this.getState());
        });
    }

    get measureMethodChoices() {
        return [
            {value: 'count', label: _t('Count')},
            {value: 'sum', label: _t('Sum')},
            {value: 'avg', label: _t('Average')},
            {value: 'min', label: _t('Minimum')},
            {value: 'max', label: _t('Maximum')},
        ];
    }

    get needsMeasureField() {
        return this.state.measureMethod !== 'count';
    }

    get measureFieldFilter() {
        return (fieldDef) => ['integer', 'float', 'monetary'].includes(fieldDef.type);
    }

    get formattedValue() {
        if (this.state.kpiValue === null) {
            return '---';
        }

        return this.state.kpiValue.toLocaleString();
    }

    getState() {
        const context = {};

        if (this.state.subtitle) {
            context.kpi_subtitle = this.state.subtitle;
        }

        context.kpi_measure_field = this.state.measureField || '__count';
        context.kpi_measure_method = this.state.measureMethod || 'count';

        let domain = [];

        try {
            domain = new Domain(this.state.domainStr).toList();
        } catch {
            // keep empty
        }

        return {
            context,
            domain,
        };
    }

    onMeasureMethodChanged(value) {
        this.state.measureMethod = value;

        if (value === 'count') {
            this.state.measureField = '__count';
        } else if (this.state.measureField === '__count') {
            this.state.measureField = '';
        }

        this._fetchKpiValue();
    }


    onMeasureFieldUpdate(path) {
        this.state.measureField = path || '';
        this._fetchKpiValue();
    }

    onSubtitleChanged(ev) {
        this.state.subtitle = ev.target.value;
    }

    onDomainUpdate(domainStr) {
        this.state.domainStr = domainStr;
        this._fetchKpiValue();
    }

    async _fetchKpiValue() {
        if (!this.props.resModel) {
            this.state.kpiValue = null;
            return;
        }

        this.state.isLoading = true;

        try {
            let domain = [];

            try {
                domain = new Domain(this.state.domainStr).toList();
            } catch {
                // keep empty
            }
            const method = this.state.measureMethod;
            const field = this.state.measureField;
            const hasField = method !== 'count' && field && field !== '__count';
            const fields = hasField ? [`${field}:${method}`] : [];

            const result = await this.orm.call(
                this.props.resModel,
                'read_group',
                [domain, fields, []],
            );

            if (result && result.length > 0) {
                if (hasField) {
                    this.state.kpiValue = result[0][field] ?? 0;
                } else {
                    this.state.kpiValue = result[0].__count || 0;
                }
            } else {
                this.state.kpiValue = 0;
            }
        } catch {
            this.state.kpiValue = null;
        }

        this.state.isLoading = false;
    }
}
