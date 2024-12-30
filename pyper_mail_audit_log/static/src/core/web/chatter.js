/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {useService} from '@web/core/utils/hooks';
import {Chatter} from '@mail/core/web/chatter';
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

        this.user = useService('user');
        this.state.isAuditLogEnabled = false;

        useEffect(() => {
            const forceLoad = this.state.isAuditLogEnabled !== this.threadService.chatterWithAuditLog;

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
        this.threadService.chatterWithAuditLog = this.state.isAuditLogEnabled;
        this.state.thread.isLoaded = false;
        this.state.thread.status = 'new';
        this.state.thread.messages = [];
    }
});
