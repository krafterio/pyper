/** @odoo-module **/

/*global L*/

import {onWillUnmount, useEffect} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {useBus, useService} from '@web/core/utils/hooks';
import {renderToString} from '@web/core/utils/render';
import {KanbanRenderer} from '@web/views/kanban/kanban_renderer';
import {Map} from './map';

export class MapRenderer extends KanbanRenderer {
    static template = 'pyper_map.MapRenderer';

    static components = {
        ...KanbanRenderer.components,
        Map,
    };

    static props = [
        ...KanbanRenderer.props,
        'bus',
        'model',
        'openRecords?',
    ];

    static defaultProps = {
        ...KanbanRenderer.defaultProps,
    };

    setup() {
        super.setup();

        this.notification = useService('notification');

        this.state.expendedSidebar = true;
        this.markers = [];
        this.selectedMarker = null;
        this.leaflet = null;

        useEffect(() => {
            if (this.leaflet) {
                this.onUpdateMap(this.leaflet);
            }
        }, () => [this.props.model.data.records]);

        useBus(this.props.bus, 'pyper-map-open-record', (event) => {
            this.selectMarker(event.detail);
        });

        onWillUnmount(() => {
            this.removeMarkers(this.leaflet);
            this.selectedMarker = null;
            this.leaflet = null;
        })
    }

    get expendedSidebar() {
        return !this.env.isSmall ? this.state.expendedSidebar : false;
    }

    toggleSidebar() {
        this.state.expendedSidebar = !this.state.expendedSidebar;
    }

    addMarkers(leaflet) {
        this.removeMarkers(leaflet);

        const markersInfo = {};
        let records = this.props.model.data.records;

        const pinInSamePlace = {};

        for (const record of records) {
            const partner = record.partner;

            if (partner && partner.partner_latitude && partner.partner_longitude) {
                const latLong = `${partner.partner_latitude}-${partner.partner_longitude}`;
                const key = `${latLong}`;

                if (key in markersInfo) {
                    markersInfo[key].record = record;
                    markersInfo[key].ids.push(record.id);
                } else {
                    pinInSamePlace[latLong] = ++pinInSamePlace[latLong] || 0;
                    markersInfo[key] = {
                        record: record,
                        ids: [record.id],
                        pinInSamePlace: pinInSamePlace[latLong],
                    };
                }
            }
        }

        for (const markerInfo of Object.values(markersInfo)) {
            const params = {
                count: markerInfo.ids.length,
                isMulti: markerInfo.ids.length > 1,
                number: this.props.model.data.records.indexOf(markerInfo.record) + 1,
                numbering: this.props.model.config.numbering,
            };

            const iconInfo = {
                className: 'o-pyper-map-marker',
                html: renderToString('pyper_map.marker', params),
            };

            const offset = markerInfo.pinInSamePlace * 0.000025;
            const marker = L.marker(
                [
                    markerInfo.record.partner.partner_latitude + offset,
                    markerInfo.record.partner.partner_longitude - offset,
                ],
                {
                    icon: L.divIcon(iconInfo),
                    ids: markerInfo.ids,
                },
            );
            marker.addTo(leaflet);
            marker.on('click', () => {
                this.openMarkerRecords(markerInfo, offset);
            });

            this.markers.push(marker);
        }
    }

    removeMarkers(leaflet) {
        for (const marker of this.markers) {
            marker.off('click');
            leaflet?.removeLayer(marker);
        }

        this.selectedMarker = null;
        this.markers = [];
    }

    selectMarker(record) {
        this.selectedMarker?._icon?.classList?.remove('selected');
        this.selectedMarker?.setZIndexOffset(0);

        const marker = this.markers.find(m => m.options.ids.includes(record.resId));

        if (marker) {
            const latlng = marker.getLatLng();
            this.leaflet?.setView(latlng, this.leaflet.getZoom());
            marker?._icon?.classList?.add('selected');
            marker.setZIndexOffset(1000);
            this.selectedMarker = marker;
        } else {
            this.notification.add(
                _t("The selected record does not have an geolocalized address."),
                {
                    type: 'info',
                },
            );
        }
    }

    getLatLng() {
        const tabLatLng = [];

        for (const record of this.props.model.data.records) {
            const partner = record.partner;

            if (partner && partner.partner_latitude && partner.partner_longitude) {
                tabLatLng.push(L.latLng(partner.partner_latitude, partner.partner_longitude));
            }
        }

        if (!tabLatLng.length) {
            return false;
        }

        return L.latLngBounds(tabLatLng);
    }

    onSetupLeaflet(leaflet) {
        this.leaflet = leaflet;
    }

    onUpdateMap(leaflet) {
        if (this.props.model.data.shouldUpdatePosition) {
            const initialCoord = this.getLatLng();

            if (initialCoord) {
                leaflet.flyToBounds(initialCoord, {animate: false});
            } else {
                leaflet.fitWorld();
            }

            leaflet.closePopup();
        }

        this.addMarkers(leaflet);
    };

    /**
     * Open the records for the specified marker.
     *
     * @param {Object} markerInfo
     * @param {Number} latLongOffset
     */
    openMarkerRecords(markerInfo, latLongOffset = 0) {
        this.props?.openRecords(markerInfo.ids, latLongOffset);
    }
}
