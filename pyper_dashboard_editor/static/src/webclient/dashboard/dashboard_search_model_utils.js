/** @odoo-module **/

/**
 * Capture the current state of the searchModel (context, domain, groupBy, orderBy, etc.)
 * Used by AddToDashboard and DashboardPreview to capture interactive view state.
 *
 * @param {Object} searchModel
 * @returns {{context: Object, domain: Array}}
 */
export function captureSearchModelState(searchModel) {
    const {domain, globalContext} = searchModel;
    const {context, groupBys, orderBy} = searchModel.getPreFavoriteValues();
    const limit = searchModel.env?.config?.pagerProps?.limit || false;
    const comparison = searchModel.comparison;

    const contextToSave = {
        ...Object.fromEntries(
            Object.entries(globalContext).filter(
                ([key]) => !key.startsWith('search_default_')
            )
        ),
        ...context,
        order_by: orderBy,
        group_by: groupBys,
    };

    if (limit) {
        contextToSave.limit = limit;
    }

    if (comparison) {
        contextToSave.comparison = comparison;
    }

    return {
        context: contextToSave,
        domain,
    };
}
