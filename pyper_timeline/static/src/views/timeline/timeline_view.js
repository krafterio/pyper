/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {TimelineArchParser} from './timeline_arch_parser';
import {TimelineController} from './timeline_controller';
import {TimelineModel} from './timeline_model';
import {TimelineRenderer} from './timeline_renderer';
import {TimelineCompiler} from './timeline_compiler';

export const timelineView = {
    type: 'timeline',

    display_name: _t('Timeline'),
    icon: 'fa fa-tasks',
    multiRecord: true,
    searchMenuTypes: ['filter', 'groupBy', 'favorite'],

    ArchParser: TimelineArchParser,
    Controller: TimelineController,
    Model: TimelineModel,
    Renderer: TimelineRenderer,
    Compiler: TimelineCompiler,

    buttonTemplate: 'pyper_timeline.TimelineView.Buttons',

    props: (props, view) => {
        const {ArchParser} = view;
        const {arch, relatedModels, resModel} = props;
        const archInfo = new ArchParser().parse(arch, relatedModels, resModel);

        return {
            ...props,
            Model: view.Model,
            Renderer: view.Renderer,
            buttonTemplate: view.buttonTemplate,
            archInfo,
        };
    },
};

registry.category('views').add('timeline', timelineView);
