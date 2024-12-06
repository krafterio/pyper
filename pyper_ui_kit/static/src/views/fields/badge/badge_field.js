/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {BadgeField} from '@web/views/fields/badge/badge_field';

patch(BadgeField, {
    defaultProps: {
        ...BadgeField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
