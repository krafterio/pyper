/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {DateTimeField} from '@web/views/fields/datetime/datetime_field';

patch(DateTimeField, {
    defaultProps: {
        ...DateTimeField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
