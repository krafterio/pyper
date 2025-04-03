/** @odoo-module **/

import {registry} from '@web/core/registry';
import {MapProvider} from '../map_provider';

export class MapboxProvider extends MapProvider {
    get attribution() {
        return `
            © <a href="https://www.mapbox.com/about/maps">Mapbox</a>
            <strong>
                <a href="https://www.mapbox.com/map-feedback" target="_blank">
                    Improve this map
                </a>
            </strong>
        `;
    }

    get isRequiredToken() {
        return true;
    }

    get tileLayerApiUrl() {
        return 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}';
    }

    get tileLayerOptions() {
        return {
            id: 'mapbox/streets-v11',
            accessToken: this.token,
        };
    }

    getGeocodingApiUrl(record) {
        const url = new URL('https://api.mapbox.com/search/geocode/v6/forward');
        url.searchParams.append('address_line1', record.street || '');
        url.searchParams.append('postcode', record.zip || '');
        url.searchParams.append('place', record.city || '');
        url.searchParams.append('region', record.state || '');
        url.searchParams.append('country', record.country_code || '');
        url.searchParams.append('limit', '1');
        url.searchParams.append('access_token', this.token);

        return url.toString();
    }

    convertGeocodingResult(result) {
        return {
            longitude: result?.features?.[0]?.geometry?.coordinates?.[0] || null,
            latitude: result?.features?.[0]?.geometry?.coordinates?.[1] || null,
        };
    }
}

registry.category('pyper_map.providers').add('mapbox', MapboxProvider);
