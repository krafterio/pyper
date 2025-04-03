/** @odoo-module **/

/*global L*/

import {loadCSS, loadJS} from '@web/core/assets';
import {registry} from '@web/core/registry';
import {session} from '@web/session';
import {Component, onWillStart, onWillUnmount, onWillUpdateProps, useEffect, useRef} from '@odoo/owl';


export class Map extends Component {
    static template = 'pyper_map.Map';

    static props = {
        mapLayerOptions: {
            type: Object,
            optional: true,
        },
        setupLeaflet: {
            type: Function,
            optional: true,
        },
        onUpdateMap: {
            type: Function,
            optional: true,
        }
    };

    static defaultProps = {
        mapLayerOptions: {},
        setupLeaflet: () => {},
    }

    setup() {
        this.mapRef = useRef('map');
        this.leaflet = null;
        this.meta = {
            provider: session['pyper_map_provider'],
            providerToken: session['pyper_map_provider_token'],
        }

        useEffect(() => {
            if (this.displayMap) {
                this.leaflet?.remove();
                this.leaflet = L.map(this.mapRef.el, {
                    maxBounds: [
                        L.latLng(180, -180),
                        L.latLng(-180, 180),
                    ],
                });

                const mapLayer = L.tileLayer(this.provider.tileLayerApiUrl, {
                    attribution: this.provider.attribution,
                    tileSize: 512,
                    zoomOffset: -1,
                    minZoom: 2,
                    maxZoom: 19,
                    ...this.provider.tileLayerOptions,
                    ...this.props.mapLayerOptions,
                });
                mapLayer.addTo(this.leaflet);

                this.props.setupLeaflet(this.leaflet, mapLayer);
            }
        }, () => [this.provider]);

        useEffect(() => {
            this.updateMap();
        });

        onWillStart(() =>
            Promise.all([
                loadJS('/pyper_map/static/lib/leaflet/leaflet-src.js'),
                loadCSS('/pyper_map/static/lib/leaflet/leaflet.css'),
            ])
        );

        onWillUpdateProps(this.onWillUpdateProps);
        onWillUnmount(this.onWillUnmount);
    }

    get providerClass() {
        return registry.category('pyper_map.providers').get(this.meta.provider, null);
    }

    get provider() {
        const provider = this.providerClass ? new this.providerClass() : null;

        if (provider) {
            provider.setup(this.meta.providerToken);
        }

        return provider;
    }

    get invalidProvider() {
        return !this.provider;
    }

    get invalidTokenProvider() {
        return this.invalidProvider || (this.provider.isRequiredToken && !this.meta.providerToken);
    }

    get displayMap() {
        return this.provider && !this.invalidProvider && !this.invalidTokenProvider;
    }

    async onWillUpdateProps() {
        this.updateMap();
    }

    onWillUnmount() {
        this.leaflet?.remove();
    }

    updateMap() {
        this.props?.onUpdateMap(this.leaflet);
    }
}
