/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {IntegerField} from '@web/views/fields/integer/integer_field';

patch(IntegerField, {
    defaultProps: {
        ...IntegerField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
