/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {browser} from '@web/core/browser/browser';
import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {RelationalModel} from '@web/model/relational_model/relational_model';
import {session} from '@web/session';

export class MapModel extends RelationalModel {
    static services = [
        ...RelationalModel.services,
        'http',
    ];

    static COORDINATE_FETCH_DELAY = 1000;

    setup(params, services) {
        super.setup(params, services);

        this.http = services.http;
        this.coordinateFetchingTimeoutHandle = null;
        this.data = reactive({
            shouldUpdatePosition: true,
            fetchingCoordinates: false,
            records: [],
        });
    }
    /**
     * @param {any} params
     * @returns {Promise<void>}
     */
    async load(params = {}) {
        if (this.coordinateFetchingTimeoutHandle) {
            this.stopFetchingCoordinates();
        }

        return await super.load(params);
    }

    stopFetchingCoordinates() {
        browser.clearTimeout(this.coordinateFetchingTimeoutHandle);

        this.coordinateFetchingTimeoutHandle = null;
        this.data.fetchingCoordinates = false;
        this.data.shouldUpdatePosition = false;
    }

    async _loadData(config) {
        const data = await super._loadData(config);

        await this._loadPartnerData(config, data);
        this._addPartnerToRecord(config, data);
        // Async fetch coordinates
        this._fetchCoordinates(config, data).then();

        this.data.records = data.records;

        return data;
    }

    async _loadPartnerData(config, data) {
        let partnerIds = [];
        data.partners = {}

        for (const record of data.records) {
            if (config.resModel === 'res.partner' && config.resPartnerField === 'id') {
                partnerIds.push(record.id);
            } else if (record[config.resPartnerField]) {
                partnerIds.push(record[config.resPartnerField].id);
            }
        }

        partnerIds = [...new Set(partnerIds)];

        if (partnerIds.length > 0) {
            const partnerData = await this.orm.searchRead(
                'res.partner',
                [['id', 'in', partnerIds]],
                ['street', 'zip', 'city', 'state_name', 'country_code', 'partner_latitude', 'partner_longitude'],
                {
                    limit: partnerIds.length,
                },
            );

            Object.assign(data.partners, partnerData.reduce((accumulator, objet) => {
                accumulator[objet.id] = objet;

                return accumulator;
            }, {}));
        }
    }

    _addPartnerToRecord(config, data) {
        for (const record of data.records) {
            if (config.resModel === 'res.partner' && config.resPartnerField === 'id') {
                record.partner = data.partners[record.id];
            } else if (record[config.resPartnerField]) {
                record.partner = data.partners[record[config.resPartnerField].id];
            }
        }
    }

    async _fetchCoordinates(config, data) {
        const fetchPartners = [];

        for (const partner of Object.values(data.partners)) {
            if (!partner['partner_latitude'] || !partner['partner_longitude']) {
                if (partner['street'] || partner['zip'] || partner['city'] || partner['state_name'] || partner['country_code']) {
                    fetchPartners.push(partner);
                }
            }
        }

        if (0 === fetchPartners.length) {
            return;
        }

        const providerName = session['pyper_map_provider'];
        const providerToken = session['pyper_map_provider_token'];
        const providerClass = registry.category('pyper_map.providers').get(providerName, null);
        const provider = providerClass ? new providerClass() : null;
        provider?.setup(providerToken);

        if (!provider) {
            return;
        }

        this.data.fetchingCoordinates = true;
        this.data.shouldUpdatePosition = true;

        const fetch = async () => {
            for (let i = 0; i < fetchPartners.length; i++) {
                await new Promise((resolve) => {
                    this.coordinateFetchingTimeoutHandle = browser.setTimeout(
                        resolve,
                        this.constructor.COORDINATE_FETCH_DELAY,
                    );
                });

                if (!this.data.fetchingCoordinates) {
                    return;
                }

                try {
                    await this._fetchCoordinatesFromAddress(provider, fetchPartners[i]);
                } catch {
                    this.notification.add(
                        _t("Geocoding Provider's request limit exceeded, try again later."),
                        {
                            type: 'danger',
                        },
                    );
                }
            }
        };

        await fetch();
        await this._writeCoordinatesUsers(config, data);
        this.data.fetchingCoordinates = false;
        this.data.shouldUpdatePosition = false;
        this.notify();
    }

    async _fetchCoordinatesFromAddress(provider, partner) {
        const res = provider.convertGeocodingResult(await this.http.get(provider.getGeocodingApiUrl(partner)));

        if (res.latitude && res.longitude) {
            partner.partner_latitude = res.latitude;
            partner.partner_longitude = res.longitude;
            partner._writeRequired = true;
        }
    }

    async _writeCoordinatesUsers(config, data) {
        const writePartners = Object.values(data.partners)
            .filter(p => p._writeRequired)
            .map(p => ({
                id: p.id,
                partner_latitude: p.partner_latitude,
                partner_longitude: p.partner_longitude,
            }));

        if (writePartners.length > 0) {
            await this.orm.call('res.partner', 'update_pyper_map_latitude_longitude', [writePartners], {
                context: config.context,
            });
        }
    }
}
