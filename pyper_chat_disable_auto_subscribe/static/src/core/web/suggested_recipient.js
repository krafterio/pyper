/* @odoo-module */


import {patch} from '@web/core/utils/patch';
import {SuggestedRecipient} from '@mail/core/web/suggested_recipient';
import {useService} from '@web/core/utils/hooks';

patch(SuggestedRecipient.prototype, {
    setup() {
        super.setup();
        this.orm = useService('orm');

        if (!this.threadService.defaultSuggestedRecipentChecked && this.props?.recipient?.checked) {
            this.props.recipient.checked = false;
        }
    },
});
