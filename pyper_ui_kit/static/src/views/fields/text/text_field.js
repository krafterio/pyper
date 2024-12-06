/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {TextField} from '@web/views/fields/text/text_field';

patch(TextField, {
    defaultProps: {
        ...TextField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
