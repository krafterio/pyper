/** @odoo-module **/

import {onMounted, onPatched} from '@odoo/owl';
import {patch} from '@web/core/utils/patch';
import {ListRenderer} from '@web/views/list/list_renderer';

const COLUMN_DEFAULT_WIDTH = '190px';

const CUSTOM_FIXED_FIELD_COLUMN_WIDTHS = {
    selector: "28px",
    priority: "30px",
    image: "30px",
    monetary: "110px",
    date: "160px",
    datetime: "160px",
    list_activity: "280px",
};

const DEFAULT_STICKYABLE_COLUMNS = [
    'display_name',
    'name',
];

patch(ListRenderer.prototype, {
    stickyableColumns: [],

    setup() {
        super.setup();

        onMounted(this.animateItems);

        onPatched(() => {
            this.forceWidthTableHeaderCells();
            this.resetStickyColumns();
            this.prepareStickyColumns();
            this.freezeStickyColumns();
            this.animateItems();
        })

        this.prepareStickyColumns();
    },

    get hasSelectors() {
        return this.props.allowSelectors;
    },

    calculateColumnWidth(column) {
        const res = super.calculateColumnWidth(column);

        if (!this.props.archInfo.fixedWidth) {
            return res;
        }

        // Replace relative column by absolute value with default value
        const type = column.widget || this.fields[column.name]?.type;

        if (res.type === 'relative') {
            res.type = 'absolute';
            res.value = CUSTOM_FIXED_FIELD_COLUMN_WIDTHS[type] || COLUMN_DEFAULT_WIDTH;
        } else if (res.type === 'absolute' && CUSTOM_FIXED_FIELD_COLUMN_WIDTHS[type]) {
            res.value = CUSTOM_FIXED_FIELD_COLUMN_WIDTHS[type];
        }

        if (typeof res.value ==='string' && !res.value.endsWith('px')) {
            res.value += 'px';
        }

        return res;
    },

    setDefaultColumnWidths() {
        super.setDefaultColumnWidths();

        if (!this.props.archInfo.fixedWidth) {
            return;
        }

        // Force to use absolute width values
        const widths = this.state.columns.map((col) => this.calculateColumnWidth(col));
        const columnOffset = this.hasSelectors ? 2 : 1;

        if (this.hasSelectors) {
            const headerSelectorEl = this.tableRef.el.querySelector(`thead th.o_list_record_selector`);

            if (headerSelectorEl) {
                headerSelectorEl.style.width = CUSTOM_FIXED_FIELD_COLUMN_WIDTHS['selector'];
            }
        }

        widths.forEach(({ type, value }, i) => {
            const headerEl = this.tableRef.el.querySelector(`th:nth-child(${i + columnOffset})`);
            if (type === 'absolute') {
                if (!this.isEmpty) {
                    headerEl.style.width = value;
                    headerEl.style.minWidth = null;
                }
            }
        });
    },

    computeColumnWidthsFromContent() {
        const headers = this.forceWidthTableHeaderCells();
        const res = super.computeColumnWidthsFromContent();

        if (!this.props.archInfo.fixedWidth) {
            return res;
        }

        // Remove the shrink of the largest columns
        headers.forEach((th) => {
            th.style.maxWidth = null;
        });

        return res;
    },

    forceWidthTableHeaderCells() {
        if (!this.props.archInfo.fixedWidth) {
            return [];
        }

        const table = this.tableRef.el;
        const headers = [...table.querySelectorAll("thead th")];

        // Force fix the width so that if the resize overflows, it doesn't affect the layout of the parent
        const tableWidth = headers.reduce((acc, th) => acc + parseFloat(th.style.width), 0);
        table.style.width = `${tableWidth}px`;

        if (!this.rootRef.el.style.width) {
            this.rootRef.el.style.width = `${Math.floor(this.rootRef.el.getBoundingClientRect().width)}px`;
        }

        return headers;
    },

    freezeColumnWidths() {
        super.freezeColumnWidths();
        this.freezeStickyColumns();
    },

    onStartResize(ev) {
        super.onStartResize(ev);
        this.freezeStickyColumns();
    },

    prepareStickyColumns() {
        const defaultStickyableCols = [];
        const stickyableCols = [];
        let colIdx = 0;

        // Make first available column like sticky
        this.state.columns.forEach((col) => {
            colIdx++;
            const colSticky = {
                index: colIdx,
                column: col,
            }

            if (col.options?.sticky) {
                stickyableCols.push(colSticky);
            }

            if (DEFAULT_STICKYABLE_COLUMNS.includes(col.name)) {
                defaultStickyableCols.push(colSticky);
            }
        });

        // Find the default stickyable column if no column is defined like sticky
        if (stickyableCols.length === 0) {
            if (defaultStickyableCols.length > 0) {
                stickyableCols.push(defaultStickyableCols[0]);
            } else if (this.state.columns.length > 0) {
                stickyableCols.push({
                    index: 1,
                    column: this.state.columns[0],
                });
            }
        }

        this.stickyableColumns = stickyableCols;
    },

    resetStickyColumns() {
        if (this.stickyableColumns.length === 0) {
            return;
        }

        const stickyColEls = this.tableRef.el.querySelectorAll('.sticky-col');
        stickyColEls.forEach((el) => {
            el.classList.remove('sticky-col');
            el.style.left = null;
        });

        this.stickyableColumns = [];
    },

    freezeStickyColumns() {
        let stickyLeft = 0;
        const stickyableColumns = []

        if (this.hasSelectors) {
            stickyableColumns.push({
                index: 1,
                column: null,
            });

            this.stickyableColumns.forEach((stickyCol) => {
                stickyableColumns.push({...stickyCol, index: stickyCol.index + 1});
            });
        } else {
            stickyableColumns.push(...this.stickyableColumns);
        }

        stickyableColumns.forEach((stickyCol) => {
            const idx = stickyCol.index;
            const stickyColEls = this.tableRef.el.querySelectorAll(`thead th:nth-child(${idx}), tbody td:nth-child(${idx}), tfoot td:nth-child(${idx})`);
            // Reset sticky left value
            let nextStickyLeft = null;

            stickyColEls.forEach((el) => {
                if (null === nextStickyLeft) {
                    nextStickyLeft += el.getBoundingClientRect().width;
                }

                el.classList.add('sticky-col');
                el.style.left = `${stickyLeft}px`;
            });

            stickyLeft += nextStickyLeft || 0;
        });

        this.removeBorderBottomLastRow();
    },

    removeBorderBottomLastRow() {
        this.tableRef.el.querySelectorAll('tbody tr.o_data_row:last-child td').forEach(td => {
            td.style.borderBottom = 'none';
        });
    },

    animateItems() {
        this.tableRef.el.querySelectorAll('tbody tr.o_group_has_content').forEach((el, idx) => {
            el.style.setProperty('--item-idx', idx);
            el.addEventListener('animationend', () => el.classList.add('clear-animation'));
        });

        this.tableRef.el.querySelectorAll('tbody tr.o_data_row').forEach((el, idx) => {
            el.style.setProperty('--item-idx', idx);
            el.addEventListener('animationend', () => el.classList.add('clear-animation'));
        });
    },
});
