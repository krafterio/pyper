/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {visitXML} from '@web/core/utils/xml';
import {ListArchParser} from '@web/views/list/list_arch_parser';
import {archParseBoolean} from '@web/views/utils';

patch(ListArchParser.prototype, {
    parse(xmlDoc, models, modelName) {
        const res = super.parse(...arguments);

        visitXML(xmlDoc, (node) => {
            if (['tree', 'list'].includes(node.tagName)) {
                res.fixedWidth = archParseBoolean(node.getAttribute('fixed_width') || '');
            }
        });

        return res;
    },
});
