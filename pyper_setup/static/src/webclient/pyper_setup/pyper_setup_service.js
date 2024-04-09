/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {evaluateExpr} from '@web/core/py_js/py';
import {registry} from '@web/core/registry';


export class PyperSetupService {
    constructor(rpc) {
        /** @type {import("@web/core/network/rpc_service").rpcService} */
        this._rpcService = rpc;
        this._registeredPrefixes = reactive({});
        this.settings = reactive({});
    }

    /**
     * Register the settings by prefix.
     *
     * @param {String} prefix
     * @param {Object} [defaultProps]
     *
     * @returns {Promise<Object>}
     */
    async register(prefix, defaultProps) {
        if (!this._registeredPrefixes.hasOwnProperty(prefix)) {
            this._registeredPrefixes[prefix] = 0;
        }

        this._registeredPrefixes[prefix] += 1;

        if (this.settings[prefix]) {
            return this.settings[prefix];
        }

        this.settings[prefix] = {};
        const paramsMap = {};

        const params = await this._rpcService('/pyper_setup/settings', {
            'prefix': prefix,
        });

        params.forEach((param) => {
            let value = param.value;

            try {
                value = evaluateExpr(value);
            } catch (e) {}

            paramsMap[param.key.substring(prefix.length)] = value;
        });

        Object.keys(defaultProps || paramsMap).forEach((propsName) => {
            this.settings[prefix][propsName] = paramsMap[propsName] || defaultProps[propsName];
        });

        return this.settings[prefix];
    }

    async unregister(prefix) {
        if (!this._registeredPrefixes.hasOwnProperty(prefix) || !this.settings.hasOwnProperty(prefix)) {
            delete this.settings[prefix];
            delete this._registeredPrefixes[prefix];

            return;
        }

        this._registeredPrefixes[prefix] -= 1;

        if (this._registeredPrefixes[prefix] <= 0) {
            delete this.settings[prefix];
            delete this._registeredPrefixes[prefix];
        }
    }

    onWillUpdateProps(prefix, nextProps) {
        if (!this.settings[prefix]) {
            return;
        }

        Object.keys(nextProps).forEach((propsName) => {
            if (this.settings[prefix].hasOwnProperty(propsName)) {
                this.settings[prefix][propsName] = nextProps[propsName] || this.settings[prefix][propsName];
            }
        });
    }
}

export const pyperSetupService = {
    dependencies: ['rpc'],
    start(env, {rpc}) {
        return reactive(new PyperSetupService(rpc));
    },
};

registry.category('services').add('pyper_setup', pyperSetupService);
