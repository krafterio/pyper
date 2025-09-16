/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {useService} from '@web/core/utils/hooks';
import {user} from '@web/core/user';
import {Chatter} from '@mail/chatter/web_portal/chatter';
import {onWillStart} from '@odoo/owl';

patch(Chatter.prototype, {
    setup() {
        super.setup();

        onWillStart(async () => {
            this.state.canWriteNotes = user.hasGroup('pyper_mail_note.group_can_write_notes');
        });
    },

    get displayNoteButton() {
        return this.props.hasMessageList && this.state.canWriteNotes;
    },
});
