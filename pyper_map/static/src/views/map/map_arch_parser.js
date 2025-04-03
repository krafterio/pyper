/** @odoo-module **/

import {visitXML} from '@web/core/utils/xml';
import {KanbanArchParser} from '@web/views/kanban/kanban_arch_parser';
import {archParseBoolean} from '@web/views/utils';

export class MapArchParser extends KanbanArchParser {
    parse(xmlDoc, models, modelName) {
        const archInfo = super.parse(xmlDoc, models, modelName);
        archInfo.resPartnerField = 'id';
        archInfo.numbering = false;

        visitXML(xmlDoc, (node) => {
            switch (node.tagName) {
                case 'pyper_map':
                    this.visitMap(node, models[modelName], archInfo);
                    break;
            }
        });

        return archInfo;
    }

    visitMap(node, fields, archInfo) {
        if (node.hasAttribute('partner_field')) {
            archInfo.resPartnerField = node.getAttribute('partner_field') || archInfo.resPartnerField;
        }

        if (archInfo.resPartnerField && 'id' !== archInfo.resPartnerField) {
            const fieldIdx = this.getNextIndex(archInfo.fieldNodes, archInfo.resPartnerField);

            if (0 === fieldIdx) {
                const partnerFieldCtx = fields[archInfo.resPartnerField].context || {};

                archInfo.fieldNodes[archInfo.resPartnerField + '_' + fieldIdx] = {
                    ...fields[archInfo.resPartnerField],
                    context: JSON.stringify(partnerFieldCtx),
                };
            }
        }

        if (node.hasAttribute('numbering')) {
            archInfo.numbering = archParseBoolean(node.getAttribute('numbering'), archInfo.numbering);
        }
    }

    getNextIndex(obj, fieldName) {
        const regex = new RegExp(`^${fieldName}_(\\d+)$`);
        let maxIndex = -1;

        for (const key in obj) {
            const match = key.match(regex);

            if (match) {
                const index = parseInt(match[1], 10);

                if (index > maxIndex) {
                    maxIndex = index;
                }
            }
        }

        return maxIndex + 1;
    }
}
