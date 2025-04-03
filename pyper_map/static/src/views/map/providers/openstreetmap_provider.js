/** @odoo-module **/

import {registry} from '@web/core/registry';
import {MapProvider} from '../map_provider';

export class MapboxProvider extends MapProvider {
    get attribution() {
        return `
            © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
        `;
    }

    get tileLayerApiUrl() {
        return 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png';
    }

    getGeocodingApiUrl(record) {
        const url = new URL('https://nominatim.openstreetmap.org/search');
        url.searchParams.append('street', record.street || '');
        url.searchParams.append('postalcode', record.zip || '');
        url.searchParams.append('city', record.city || '');
        url.searchParams.append('state', record.state || '');
        url.searchParams.append('country', record.country_code || '');
        url.searchParams.append('limit', '1');
        url.searchParams.append('format', 'jsonv2');

        return url.toString();
    }

    convertGeocodingResult(result) {
        return {
            longitude: result?.[0]?.lon || null,
            latitude: result?.[0]?.lat || null,
        };
    }
}

registry.category('pyper_map.providers').add('openstreetmap', MapboxProvider);
