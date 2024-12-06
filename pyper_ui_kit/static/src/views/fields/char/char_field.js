/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {CharField} from '@web/views/fields/char/char_field';

patch(CharField, {
    defaultProps: {
        ...CharField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
