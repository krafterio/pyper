import {registry} from "@web/core/registry";
import {session} from "@web/session";
import {Setting} from "@web/views/form/setting/setting";

import {Component} from "@odoo/owl";
import {standardWidgetProps} from "@web/views/widgets/standard_widget_props";

class ResConfigPyperEdition extends Component {
    static template = "res_config_pyper_edition";
    static components = { Setting };
    static props = {
        ...standardWidgetProps,
    };

    setup() {
        this.serverVersion = session.server_version;
    }
}

export const resConfigPyperEdition = {
    component: ResConfigPyperEdition,
};

registry.category("view_widgets").add("res_config_pyper_edition", resConfigPyperEdition);
