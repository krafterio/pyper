/** @odoo-module **/

import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';

import {Component, useChildSubEnv, useState} from '@odoo/owl';

class OrganizationSelector {
    constructor(organizationService, toggleDelay) {
        this.organizationService = organizationService;
        this.selectedOrganizationsIds = organizationService.activeOrganizationIds.slice();

        this._debouncedApply = debounce(() => this._apply(), toggleDelay);
    }

    get allOrganizationIds() {
        return Object.values(this.organizationService.allowedOrganizations).map((x) => x.id);
    }

    get isAllOrganizationsSelected() {
        return this.allOrganizationIds.every((elem) => this.selectedOrganizationsIds.includes(elem));
    }

    isOrganizationSelected(organizationId) {
        return this.selectedOrganizationsIds.includes(organizationId);
    }

    switchOrganization(mode, organizationId) {
        if (mode === 'toggle_all') {
            if (this.isAllOrganizationsSelected) {
                this.allOrganizationIds.forEach((organizationId) => this._deselectOrganization(organizationId));
                this._selectOrganization(organizationId);
                this._apply();
            } else {
                this.allOrganizationIds.forEach((organizationId) => this._selectOrganization(organizationId));
                this._apply();
            }
        } else if (mode === 'toggle') {
            if (this.selectedOrganizationsIds.includes(organizationId)) {
                this._deselectOrganization(organizationId);
            } else {
                this._selectOrganization(organizationId);
            }
            this._debouncedApply();
        } else if (mode === 'loginto') {
            this.selectedOrganizationsIds.splice(0, this.selectedOrganizationsIds.length);
            this._selectOrganization(organizationId);
            this._apply();
        }
    }

    _selectOrganization(organizationId) {
        if (!this.selectedOrganizationsIds.includes(organizationId)) {
            this.selectedOrganizationsIds.push(organizationId);
        }
    }

    _deselectOrganization(organizationId) {
        if (this.selectedOrganizationsIds.includes(organizationId)) {
            this.selectedOrganizationsIds.splice(this.selectedOrganizationsIds.indexOf(organizationId), 1);
        }
    }

    _apply() {
        this.organizationService.setOrganizations(this.selectedOrganizationsIds);
    }
}

export class SwitchOrganizationItem extends Component {
    static template = 'pyper_organization.SwitchOrganizationItem';

    static components = {
        DropdownItem,
        SwitchOrganizationItem,
    };

    static props = {
        organization: {},
    };

    setup() {
        this.organizationService = useService('organization');
        this.organizationSelector = useState(this.env.organizationSelector);
    }

    get isOrganizationSelected() {
        return this.organizationSelector.isOrganizationSelected(this.props.organization.id);
    }

    get isOrganizationAllowed() {
        return this.props.organization.id in this.organizationService.allowedOrganizations;
    }

    get isCurrent() {
        return this.props.organization.id === this.organizationService.currentOrganization.id;
    }

    logIntoOrganization() {
        if (this.isOrganizationAllowed) {
            this.organizationSelector.switchOrganization('loginto', this.props.organization.id);
        }
    }

    toggleOrganization() {
        if (this.isOrganizationAllowed) {
            this.organizationSelector.switchOrganization('toggle', this.props.organization.id);
        }
    }
}

export class SwitchOrganizationMenu extends Component {
    static template = 'pyper_organization.SwitchOrganizationMenu';

    static components = {
        Dropdown,
        DropdownItem,
        SwitchOrganizationItem,
    };

    static props = {};

    static toggleDelay = 1000;

    setup() {
        this.organizationService = useService('organization');

        this.organizationSelector = useState(
            new OrganizationSelector(this.organizationService, this.constructor.toggleDelay)
        );
        useChildSubEnv({organizationSelector: this.organizationSelector});
    }

    get isAllOrganizationsSelected() {
        return this.organizationSelector.isAllOrganizationsSelected;
    }

    get organizationInitials() {
        return this.organizationService.currentOrganization.initials;
    }

    get organizationLogo() {
        return this.organizationService.currentOrganization.logo_data;
    }

    toggleAllOrganizations() {
        this.organizationSelector.switchOrganization('toggle_all', this.organizationService.currentOrganization.id);
    }
}

export const systrayItem = {
    Component: SwitchOrganizationMenu,
    isDisplayed(env) {
        const {allowedOrganizations} = env.services.organization;

        return Object.keys(allowedOrganizations).length > 0;
    },
};

registry.category('systray').add('SwitchOrganizationMenu', systrayItem, {sequence: 0});
