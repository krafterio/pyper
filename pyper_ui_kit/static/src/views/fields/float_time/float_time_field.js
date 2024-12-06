/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {FloatTimeField} from '@web/views/fields/float_time/float_time_field';

patch(FloatTimeField, {
    defaultProps: {
        ...FloatTimeField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
