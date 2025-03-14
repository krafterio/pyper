/* @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

export const messageActionsRegistry = registry.category("mail.message/actions");

messageActionsRegistry
    .add("edit activity", {
        condition: (component) => component.canEditActivity,
        icon: "fa fa-pencil",
        title: _t("Edit Activity"),
        onClick: (component) => component.onClickEditActivity(),
        sequence: 80,
    })