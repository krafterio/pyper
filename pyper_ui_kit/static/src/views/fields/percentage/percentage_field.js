/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {PercentageField} from '@web/views/fields/percentage/percentage_field';

patch(PercentageField, {
    defaultProps: {
        ...PercentageField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
