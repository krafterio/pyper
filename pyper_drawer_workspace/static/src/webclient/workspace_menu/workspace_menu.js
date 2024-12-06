/** @odoo-module **/

import {Component, useChildSubEnv, useState} from '@odoo/owl';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';

class WorkspaceSelector {
    constructor(companyService, toggleDelay) {
        this.companyService = companyService;
        this.selectedWorkspacesIds = companyService.activeCompanyIds.slice();

        this._debouncedApply = debounce(() => this._apply(), toggleDelay);
    }

    get allWorkspaceIds() {
        return Object.values(this.companyService.allowedCompanies).map((x) => x.id);
    }

    get isAllWorkspacesSelected() {
        return this.allWorkspaceIds.every((elem) => this.selectedWorkspacesIds.includes(elem));
    }

    isWorkspaceSelected(workspaceId) {
        return this.selectedWorkspacesIds.includes(workspaceId);
    }

    switchWorkspace(mode, workspaceId) {
        if (mode === 'toggle_all') {
            if (this.isAllWorkspacesSelected) {
                this.allWorkspaceIds.forEach((workspaceId) => this._deselectWorkspace(workspaceId));
                this._selectWorkspace(workspaceId);
                this._apply();
            } else {
                this.allWorkspaceIds.forEach((workspaceId) => this._selectWorkspace(workspaceId));
                this._apply();
            }
        } else if (mode === 'toggle') {
            if (this.selectedWorkspacesIds.includes(workspaceId)) {
                this._deselectWorkspace(workspaceId);
            } else {
                this._selectWorkspace(workspaceId);
            }
            this._debouncedApply();
        } else if (mode === 'loginto') {
            this.selectedWorkspacesIds.splice(0, this.selectedWorkspacesIds.length);
            this._selectWorkspace(workspaceId);
            this._apply();
        }
    }

    _selectWorkspace(workspaceId) {
        if (!this.selectedWorkspacesIds.includes(workspaceId)) {
            this.selectedWorkspacesIds.push(workspaceId);
        }
    }

    _deselectWorkspace(workspaceId) {
        if (this.selectedWorkspacesIds.includes(workspaceId)) {
            this.selectedWorkspacesIds.splice(this.selectedWorkspacesIds.indexOf(workspaceId), 1);
        }
    }

    _apply() {
        this.companyService.setCompanies(this.selectedWorkspacesIds);
    }
}

export class WorkspaceMenuGlobalCounter {
    get counter() {
        return 0;
    }
}

export class WorkspaceMenuItem extends Component {
    static template = 'pyper_drawer_workspace.WorkspaceMenuItem';

    static components = {
        DropdownItem,
        WorkspaceMenuItem,
    };

    static props = {
        workspace: {
            type: Object,
        },
        selector: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        selector: false,
    }

    setup() {
        this.companyService = useService('company');
        this.workspaceSelector = useState(this.env.workspaceSelector);
    }

    get isWorkspaceSelected() {
        return this.workspaceSelector.isWorkspaceSelected(this.props.workspace.id);
    }

    get isWorkspaceAllowed() {
        return this.props.workspace.id in this.companyService.allowedCompanies;
    }

    get isCurrent() {
        return this.props.workspace.id === this.companyService.currentCompany.id;
    }

    logIntoWorkspace() {
        if (this.isWorkspaceAllowed) {
            this.workspaceSelector.switchWorkspace('loginto', this.props.workspace.id);
        }
    }

    toggleWorkspace() {
        if (this.isWorkspaceAllowed) {
            this.workspaceSelector.switchWorkspace('toggle', this.props.workspace.id);
        }
    }
}

export class WorkspaceSettingsItem extends Component {
    static template = 'pyper_drawer_workspace.WorkspaceSettingsItem';

    static components = {
        DropdownItem,
    }

    static props = {
        menu: {
            type: Object,
        },
    }

    setup() {
        this.drawerService = useState(useService('drawer'));
    }

    onSelected() {
        if (this.props.menu.children.length === 0) {
            this.drawerService.selectMenu(this.props.menu);

            return;
        }

        if (this.props.menu?.id !== this.drawerService.subPanelMenu?.id) {
            this.drawerService.openSubPanel(this.props.menu);
        } else {
            this.drawerService.closeSubPanel();
        }
    }
}

export class WorkspaceMenu extends Component {
    static template = 'pyper_drawer_workspace.WorkspaceMenu';

    static components = {
        Dropdown,
        DropdownItem,
        WorkspaceMenuItem,
        WorkspaceSettingsItem,
    };

    static props = {
        selector: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        selector: false,
    }

    static toggleDelay = 1000;

    setup() {
        this.companyService = useState(useService('company'));
        this.workspaceSelector = useState(new WorkspaceSelector(this.companyService, this.constructor.toggleDelay));
        this.menuService = useState(useService('menu'));
        this.menuStateService = useState(useService('menu_state'));
        this.systemTrayItems = registry.category('workspace_menu_systray').getAll();
        this.systemTrayGloalCounters = useState([]);

        this.systemTrayItems.forEach(item => {
            if (item.counterService) {
                const counterService = useState(useService(item.counterService));

                if (counterService instanceof WorkspaceMenuGlobalCounter) {
                    this.systemTrayGloalCounters.push(counterService);
                }
            }
        });

        useChildSubEnv({workspaceSelector: this.workspaceSelector});
    }

    get isAllWorkspacesSelected() {
        return this.workspaceSelector.isAllWorkspacesSelected;
    }

    get workspaceInitials() {
        return this.companyService.currentCompany?.initials;
    }

    get workspaceLogo() {
        return this.this.companyService.currentCompany.logo_data || undefined;
    }

    get workspaceName() {
        return this.companyService.currentCompany?.name;
    }

    get allowedWorkspaces() {
        return Object.values(this.companyService.allowedCompanies)
            .filter((c) => !c.parent_id)
            .sort((c1, c2) => c1.sequence - c2.sequence);
    }

    get menuItems() {
        const menu = this.menuService.getMenuAsTree('root');
        const items = [];

        (menu.childrenTree || []).forEach((menu) => {
            if ('workspace_menu' === menu.position) {
                items.push({
                    ...menu,
                    isActive: this.menuStateService.menuIsActivated(menu),
                });
            }
        });

        return items;
    }

    get globalCounter() {
        let counter = 0;

        this.systemTrayGloalCounters.forEach(globalCounter => {
            counter += globalCounter.counter;
        });

        return counter;
    }

    toggleAllWorkspaces() {
        this.workspaceSelector.switchWorkspace('toggle_all', this.companyService.currentCompany.id);
    }
}

export const systrayWorkspaceMenu = {
    Component: WorkspaceMenu,
    isDisplayed() {
        return false;
    },
};

registry.category('systray').add('WorkspaceMenu', systrayWorkspaceMenu, {sequence: 0});
