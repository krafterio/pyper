/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {_t} from '@web/core/l10n/translation';
import {Many2ManyTagsField} from '@web/views/fields/many2many_tags/many2many_tags_field';

patch(Many2ManyTagsField, {
    defaultProps: {
        ...Many2ManyTagsField.defaultProps,
        placeholder: _t('Select values'),
    },
});
