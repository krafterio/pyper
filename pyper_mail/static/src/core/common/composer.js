/* @odoo-module */

import { Composer } from "@mail/core/common/composer";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(Composer.prototype, {
    async setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.state.activityTypes = await this.getAllActivityTypes();
    },

    async getAllActivityTypes() {
        const res = await this.orm.searchRead("mail.activity.type", [], ["name"]);
        return res;
    },

    updateSelectedType(ev) {
        const selectedTypeId = ev.target.value;
        const selectedType = this.state.activityTypes.find(type => type.id === parseInt(selectedTypeId));
        this.state.selectedType = selectedType;
    },

    async editMessage(ev) {
        if (this.props.composer.message.mail_activity_type_name && this.state.selectedType) {
            await this.updateType(this.state.selectedType);
            this.props.composer.message.mail_activity_type_name = this.state.selectedType.name;
        }
        super.editMessage(ev);
    },
    async updateType(type) {
        await this.orm.write('mail.message', [this.props.composer.message.id], { mail_activity_type_id: type.id });

    }
});