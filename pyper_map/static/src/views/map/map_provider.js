/** @odoo-module **/

export class MapProvider {
    setup(token) {
        this.token = token;
    }

    /**
     * @return {String|undefined}
     */
    get attribution() {
        return undefined;
    }

    get isRequiredToken() {
        return false;
    }

    /**
     * @return {String}
     */
    get tileLayerApiUrl() {
        throw Error('The apiTilesUrl property of MapProvider must be override');
    }

    get tileLayerOptions() {
        return {};
    }

    /**
     *
     * @param {Object} record
     * @return {String}
     */
    getGeocodingApiUrl(record) {
        throw Error('The getGeocodingApiUrl method of MapProvider must be override');
    }

    /**
     *
     * @param {any} result
     * @return {Object}
     */
    convertGeocodingResult(result) {
        return {
            longitude: null,
            latitude: null,
        };
    }
}
