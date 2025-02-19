/* @odoo-module */

import {Message} from "@mail/core/common/message";
import {useService} from "@web/core/utils/hooks";
import {patch} from "@web/core/utils/patch";

patch(Message.prototype, {
    async setup() {
        super.setup();
        this.orm = useService("orm");
        this.isAdmin = await useService("user").hasGroup("base.group_system");
    },

    get canEditActivity() {
        if (!this.props.message.mail_activity_type_name)
            return false;
        return this.userService.userId === this.props.message.author.user.id || this.isAdmin;
    },
});
