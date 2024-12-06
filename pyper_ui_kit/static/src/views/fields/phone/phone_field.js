/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {PhoneField} from '@web/views/fields/phone/phone_field';

patch(PhoneField, {
    defaultProps: {
        ...PhoneField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
