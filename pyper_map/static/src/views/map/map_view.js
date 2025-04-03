/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {MapArchParser} from './map_arch_parser';
import {MapController} from './map_controller';
import {MapModel} from './map_model';
import {MapRenderer} from './map_renderer';
import {MapCompiler} from './map_compiler';

export const mapView = {
    type: 'pyper_map',
    display_name: _t('Map'),
    icon: 'fa fa-map-marker',
    multiRecord: true,

    ArchParser: MapArchParser,
    Controller: MapController,
    Model: MapModel,
    Renderer: MapRenderer,
    Compiler: MapCompiler,

    buttonTemplate: 'pyper_map.MapView.Buttons',

    searchMenuTypes: ['filter', 'favorite'],

    props: (genericProps, view) => {
        const {arch, relatedModels, resModel} = genericProps;
        const {ArchParser} = view;
        const archInfo = new ArchParser().parse(arch, relatedModels, resModel);
        const defaultGroupBy = genericProps.searchMenuTypes.includes('groupBy') && archInfo.defaultGroupBy;

        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            Compiler: view.Compiler,
            buttonTemplate: view.buttonTemplate,
            archInfo,
            defaultGroupBy,
        };
    },
};

registry.category('views').add('pyper_map', mapView);
