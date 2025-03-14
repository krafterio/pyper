/* @odoo-module */

import { Message } from "@mail/core/common/message";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";

patch(Message.prototype, {
    async setup() {
        super.setup();
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        this.isAdmin = await useService("user").hasGroup("base.group_system");
    },

    get canEditActivity() {
        if (!this.props.message.mail_activity_type_name)
            return false;
        return this.userService.userId === this.props.message.author.user.id || this.isAdmin;
    },

    async getViewId() {
        const views = await this.orm.searchRead(
            "ir.ui.view",
            [["name", "=", "mail.message.edit.form"]],
            ["id"]
        )
        if (!views)
            return false;
        return views[0].id;
    },

    async onClickEdit() {
        await this.onClickEditActivity()
    },


    async onClickEditActivity() {
        const resId = await this.getViewId();
        if (!resId)
            return;
        this.dialogService.add(FormViewDialog, {
            resModel: "mail.message",
            resId: this.props.message.id,
            viewId: resId,
            onRecordSaved: (record) => {
                this.action.doAction({
                    type: "ir.actions.act_window_close",
                });
                window.location.reload();
            },

        });
    },
});

