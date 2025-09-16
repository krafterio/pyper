/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {useService} from '@web/core/utils/hooks';
import {Chatter} from '@mail/chatter/web_portal/chatter';
import {onWillUpdateProps, useEffect} from '@odoo/owl';

patch(Chatter.prototype, {
    setup() {
        onWillUpdateProps((nextProps) => {
            if (this.props.threadId !== nextProps.threadId || this.props.threadModel !== nextProps.threadModel) {
                this.state.isAuditLogEnabled = false;
                this._resetThread();
            }
        });

        super.setup();

        this.state.isAuditLogEnabled = false;

        useEffect(() => {
            const forceLoad = this.state.isAuditLogEnabled !== this.state.thread.chatterWithAuditLog;

            if (!forceLoad) {
                return;
            }

            this._resetThread();
            this.load(this.state.thread, ['messages', 'followers', 'attachments', 'suggestedRecipients']);
        }, () => [this.state.isAuditLogEnabled]);
    },

    onClickAuditLog() {
        this.state.isAuditLogEnabled = !this.state.isAuditLogEnabled;
    },

    _resetThread() {
        this.state.thread.chatterWithAuditLog = this.state.isAuditLogEnabled;
        this.state.thread.isLoaded = false;
        this.state.thread.status = 'new';
        this.state.thread.messages = [];
    }
});
