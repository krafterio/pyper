/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {FloatField} from '@web/views/fields/float/float_field';

patch(FloatField, {
    defaultProps: {
        ...FloatField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
