/** @odoo-module */

import {Dialog} from '@web/core/dialog/dialog';
import {patch} from '@web/core/utils/patch';

patch(Dialog, {
    defaultProps: {
        ...Dialog.defaultProps,
        title: 'Pyper',
    },
});
