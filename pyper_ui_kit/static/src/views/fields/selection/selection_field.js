/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {SelectionField} from '@web/views/fields/selection/selection_field';

patch(SelectionField, {
    defaultProps: {
        ...SelectionField.defaultProps,
        placeholder: _t('Select a value'),
    },
});
