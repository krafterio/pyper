/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {MonetaryField} from '@web/views/fields/monetary/monetary_field';

patch(MonetaryField, {
    defaultProps: {
        ...MonetaryField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
