/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {Many2OneField} from '@web/views/fields/many2one/many2one_field';

patch(Many2OneField, {
    defaultProps: {
        ...Many2OneField.defaultProps,
        placeholder: _t('Select a value'),
    },
});
