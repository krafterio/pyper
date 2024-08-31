/** @odoo-module **/

/**
 * Sort the dashboards by categories and move dashboards without category to the end.
 *
 * @param {Object[]} boards The dashboard.dashboard instances
 *
 * @return {Object[]} The sorted dashboards
 */
export const orderDashboards = function(boards) {
    boards.sort((a, b) => {
        if (a.category_id === false && b.category_id !== false) {
            return 1;
        }

        if (a.category_id !== false && b.category_id === false) {
            return -1;
        }

        return 0;
    });

    return boards;
};
