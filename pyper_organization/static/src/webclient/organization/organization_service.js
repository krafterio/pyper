/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {browser} from '@web/core/browser/browser';
import {cookie} from '@web/core/browser/cookie';
import {UPDATE_METHODS} from '@web/core/orm_service';
import {registry} from '@web/core/registry';
import {session} from '@web/session';

const OIDS_HASH_SEPARATOR = '-';

function parseOrganizationIds(oids, separator = OIDS_HASH_SEPARATOR) {
    if (typeof oids === 'string') {
        return oids.split(separator).map(Number);
    } else if (typeof oids === 'number') {
        return [oids];
    }
    return [];
}

function formatOrganizationIds(oids, separator = OIDS_HASH_SEPARATOR) {
    return oids.join(separator);
}

function computeActiveOrganizationIds(oids, activeCompanyIds) {
    const {user_organizations} = session;
    let activeOrganizationIds = oids || [];
    const availableOrganizationsFromSession = user_organizations.allowed_organizations;

    Object.values(availableOrganizationsFromSession).forEach((k) => {
        if (!activeCompanyIds.includes(k.company_id)) {
            delete availableOrganizationsFromSession[k.id];
        }
    });

    const notAllowedOrganizations = activeOrganizationIds.filter(
        (id) => !(id in availableOrganizationsFromSession)
    );

    if (!activeOrganizationIds.length || notAllowedOrganizations.length) {
        if (Object.keys(availableOrganizationsFromSession).length > 0) {
            const organizations = Object.values(availableOrganizationsFromSession)
                .sort((a, b) => a.sequence - b.sequence);

            activeOrganizationIds = [organizations[0].id]
        } else {
            activeOrganizationIds = user_organizations.current_organization ? [user_organizations.current_organization] : [];
        }
    }

    return activeOrganizationIds;
}

function getOrganizationIdsFromBrowser(hash) {
    let oids;

    if ('oids' in hash) {
        oids = parseOrganizationIds(hash.oids, OIDS_HASH_SEPARATOR);
    } else if (cookie.get('oids')) {
        oids = parseOrganizationIds(cookie.get('oids'));
    }

    return oids || [];
}


export class OrganizationState {
    constructor(env, user, router, action) {
        this.env = env;
        this.user = user;
        this.router = router;
        this.action = action;
    }

    setup() {
        this.state = {
            mounted: false,
        };

        const allowedOrganizations = session.user_organizations.allowed_organizations;
        const activeOrganizationIds = computeActiveOrganizationIds(
            getOrganizationIdsFromBrowser(this.router.current.hash),
            Object.values(this.user.context.allowed_company_ids || {})
        );

        // update browser data
        const oidsHash = formatOrganizationIds(activeOrganizationIds, OIDS_HASH_SEPARATOR);
        this.router.replaceState({oids: oidsHash}, {lock: true});
        cookie.set('oids', formatOrganizationIds(activeOrganizationIds));
        this.user.updateContext({allowed_organization_ids: activeOrganizationIds});

        // reload the page if changes are being done to `organization`
        this.env.bus.addEventListener('RPC:RESPONSE', (ev) => {
            const {data, error} = ev.detail;
            const {model, method} = data.params;

            if (!error && model === 'organization' && UPDATE_METHODS.includes(method)) {
                if (!browser.localStorage.getItem('running_tour')) {
                    this.action.doAction('reload_context');
                }
            }
        });

        this.allowedOrganizations = allowedOrganizations;
        this._activeOrganizationIds = activeOrganizationIds;
    }

    get activeOrganizationIds() {
        return this._activeOrganizationIds.slice();
    }

    get currentOrganization() {
        return this.allowedOrganizations[this.activeOrganizationIds[0]];
    }

    getOrganization(organizationId) {
        return this.allowedOrganizations[organizationId];
    }

    /**
     * @param {Array<>} organizationIds - List of organizations to log into
     */
    setOrganizations(organizationIds) {
        const newOrganizationIds = organizationIds.length ? organizationIds : [this.activeOrganizationIds[0]];

        function addOrganizations(organizationIds) {
            for (const organizationId of organizationIds) {
                if (!newOrganizationIds.includes(organizationId)) {
                    newOrganizationIds.push(organizationId);
                }
            }
        }

        const oidsHash = formatOrganizationIds(newOrganizationIds, OIDS_HASH_SEPARATOR);
        this.router.pushState({oids: oidsHash}, {lock: true});
        this.router.pushState({_organization_switching: true});
        cookie.set('oids', formatOrganizationIds(newOrganizationIds));
        browser.setTimeout(() => browser.location.reload()); // history.pushState is a little async
    }
}

export const organizationService = {
    dependencies: ['user', 'router', 'action'],
    start(env, {user, router, action}) {
        const organizationState = reactive(new OrganizationState(env, user, router, action));
        organizationState.setup();

        return organizationState;
    },
};

registry.category('services').add('organization', organizationService);
