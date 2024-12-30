/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {useService} from '@web/core/utils/hooks';
import {Chatter} from '@mail/core/web/chatter';
import {onWillStart} from '@odoo/owl';

patch(Chatter.prototype, {
    setup() {
        super.setup();
        this.user = useService('user');

        onWillStart(async () => {
            this.state.canWriteNotes = await this.user.hasGroup('pyper_web_theme_activity.group_can_write_notes');
        });
    },
});
