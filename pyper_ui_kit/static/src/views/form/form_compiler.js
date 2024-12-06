/** @odoo-module **/

import {registry} from '@web/core/registry';
import {append, createElement} from '@web/core/utils/xml';
import {getModifier} from '@web/views/view_compiler';


/**
 * @param {Element} node
 * @param {Record<string, any>} params
 * @returns {Element|String}
 */
function compileButtonActions(node, params) {
    if (!node.children.length || !params.isSubView) {
        return '';
    }

    const buttonActions = createElement('ButtonActions');

    let slotId = 0;
    let hasContent = false;

    for (const child of node.children) {
        const invisible = getModifier(child, 'invisible');

        if (!params.compileInvisibleNodes && (invisible === 'True' || invisible === '1')) {
            continue;
        }

        hasContent = true;
        let isVisibleExpr;

        if (!invisible || invisible === 'False' || invisible === '0') {
            isVisibleExpr = 'true';
        } else if (invisible === "True" || invisible === "1") {
            isVisibleExpr = "false";
        } else {
            isVisibleExpr = `!__comp__.evaluateBooleanExpr(${JSON.stringify(
                invisible
            )},__comp__.props.record.evalContextWithVirtualIds)`;
        }

        const mainSlot = createElement("t", {
            't-set-slot': `slot_${slotId++}`,
            isVisible: isVisibleExpr,
        });

        if (child.tagName === 'button' || child.children.tagName === 'button') {
            child.classList.add('oe_button_action');

            // The classes 'oe_highlight' and 'oe_link' are converted into 'btn-primary' and 'btn-link' classes
            // by odooToBootstrapClasses of ViewButton component
            if (!child.classList.contains('oe_highlight') && !child.classList.contains('oe_link')) {
                child.classList.add('btn-outline-secondary');
            }
        }

        if (child.tagName === 'field') {
            child.classList.add('d-inline-block', 'mb-0', 'z-index-0');
        }

        append(mainSlot, this.compileNode(child, params, false));
        append(buttonActions, mainSlot);
    }

    return hasContent ? buttonActions : '';
}

registry.category('form_compilers').add('button_actions_compiler', {
    selector: 'header',
    fn: compileButtonActions,
});
