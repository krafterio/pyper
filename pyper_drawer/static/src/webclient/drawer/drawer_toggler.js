/** @odoo-module **/

import {Component, onWillStart, onWillUpdateProps, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {evaluateExpr} from '@web/core/py_js/py';


export class DrawerToggler extends Component {
    static template = 'pyper_drawer.DrawerToggler';

    static props = {
        autoHide: {
            type: Boolean,
            optional: true,
        },
        useCaretIcon: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        autoHide: undefined,
        useCaretIcon: undefined,
    };

    static configurableDefaultProps = {
        autoHide: false,
        useCaretIcon: false,
    };

    static SETTINGS_KEY_PREFIX = 'pyper_drawer.drawer_toggler_props.';

    setup() {
        this.rpc = useService('rpc');
        this.drawerService = useState(useService('drawer'));
        this.initialSettings = useState({});
        this.settings = useState({});

        onWillStart(async () => {
            const params = await this.rpc('/drawer/settings', {});
            const paramsMap = {};

            params.forEach((param) => {
                paramsMap[param.key.substring(DrawerToggler.SETTINGS_KEY_PREFIX.length)] = evaluateExpr(param.value);
            });

            Object.keys(DrawerToggler.configurableDefaultProps).forEach((props) => {
                if (paramsMap.hasOwnProperty(props)) {
                    this.initialSettings[props] = paramsMap[props];
                }

                this.settings[props] = this._getConfigurablePropsValue(props);
            });
        });

        onWillUpdateProps((nextProps) => {
            Object.keys(DrawerToggler.configurableDefaultProps).forEach((props) => {
                this.settings[props] = this._getConfigurablePropsValue(props, nextProps);
            });
        });
    }

    get classes() {
        return {
            'o-dropdown': true,
            'dropdown': true,
            'o_drawer_toggler': true,
            'o-dropdown--no-caret': true,
            'o_drawer--locked': this.drawerService.isLocked,
            'o_drawer--mini': this.drawerService.isMinified,
            'o_drawer--fixed-top': this.drawerService.isFixedTop,
        };
    }

    get displayMenuIcon() {
        return !this.settings.useCaretIcon || (this.settings.useCaretIcon && !this.drawerService.isMinified);
    }

    get displayCaretIcon() {
        return this.settings.useCaretIcon && this.drawerService.isMinified;
    }

    get display() {
        return !(this.settings.autoHide && this.drawerService.isLocked) && !this.drawerService.disabledOnSmallScreen;
    }

    onClick() {
        this.drawerService.toggle();
    }

    _getConfigurablePropsValue(props, nextProps) {
        const allProps = nextProps || this.props;

        if (undefined !== allProps[props]) {
            return allProps[props];
        }

        if (this.initialSettings.hasOwnProperty(props) && ![null, '', undefined].includes(this.initialSettings[props])) {
            return this.initialSettings[props];
        }

        return DrawerToggler.configurableDefaultProps[props];
    }
}
