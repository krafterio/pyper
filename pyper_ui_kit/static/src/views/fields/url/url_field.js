/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {UrlField} from '@web/views/fields/url/url_field';

patch(UrlField, {
    defaultProps: {
        ...UrlField.defaultProps,
        placeholder: _t('Enter a value'),
    },
});
