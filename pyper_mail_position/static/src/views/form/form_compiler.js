/* @odoo-module */

import {onWillStart, onWillDestroy} from '@odoo/owl';
import {FormCompiler} from '@web/views/form/form_compiler';
import {SIZES} from '@web/core/ui/ui_service';
import {patch} from '@web/core/utils/patch';
import {useService} from '@web/core/utils/hooks';
import {append, setAttributes} from '@web/core/utils/xml';

patch(FormCompiler.prototype, {
    setup() {
        super.setup();
        this.pyperSetupService = useService('pyper_setup');

        onWillStart(async () => {
            await this.pyperSetupService.register('pyper_mail_position.', {
                chatterPosition: undefined,
            });
        });

        onWillDestroy(() => {
            this.pyperSetupService.unregister('pyper_mail_position.');
        });
    },

    get chatterPosition() {
        return this.pyperSetupService.settings['pyper_mail_position.']?.chatterPosition || 'auto';
    },

    compile(node, params) {
        const res = super.compile(node, params);
        const chatterPosition = this.chatterPosition;

        // Default behavior
        if ('auto' === chatterPosition) {
            return res;
        }

        const webClientViewAttachmentViewHookXml = res.querySelector('.o_attachment_preview');
        const chatterContainerHookXml = res.querySelector('.o-mail-Form-chatter:not(.o-isInFormSheetBg)');

        if (!chatterContainerHookXml) {
            // No chatter
            return res;
        }

        const chatterContainerXml = chatterContainerHookXml.querySelector("t[t-component='__comp__.mailComponents.Chatter']");
        const formSheetBgXml = res.querySelector('.o_form_sheet_bg');
        const parentXml = formSheetBgXml && formSheetBgXml.parentNode;

        if (!parentXml) {
            // No form sheet bg
            return res;
        }

        if ('sided' === chatterPosition) {
            setAttributes(chatterContainerXml, {
                isInFormSheetBg: `__comp__.uiService.size < ${SIZES.XXL}`,
                isChatterAside: `__comp__.uiService.size >= ${SIZES.XXL}`,
            });
            setAttributes(chatterContainerHookXml, {
                "t-attf-class": `{{ __comp__.uiService.size >= ${SIZES.XXL} ? "o-aside" : "" }}`,
            });
        } else if (chatterPosition === 'bottom') {
            // Keep the chatter in form sheet (the one used for the attachment viewer case)
            // Otherwise if it's not there, create it
            if (webClientViewAttachmentViewHookXml) {
                const sheetBgChatterContainerHookXml = res.querySelector('.o-mail-Form-chatter.o-isInFormSheetBg');

                setAttributes(sheetBgChatterContainerHookXml, {
                    't-if': 'true',
                });
                setAttributes(chatterContainerHookXml, {
                    't-if': 'false',
                });
            } else {
                const sheetBgChatterContainerHookXml = chatterContainerHookXml.cloneNode(true);
                sheetBgChatterContainerHookXml.classList.add('o-isInFormSheetBg');

                setAttributes(sheetBgChatterContainerHookXml, {
                    "t-if": 'true',
                    "t-attf-class": `{{ (__comp__.uiService.size >= ${SIZES.XXL} && ${
                        chatterPosition !== "bottom"
                    }) ? "o-aside" : "o-bottom" }}`,
                });

                append(formSheetBgXml, sheetBgChatterContainerHookXml);
                const sheetBgChatterContainerXml = sheetBgChatterContainerHookXml.querySelector("t[t-component='__comp__.mailComponents.Chatter']");

                setAttributes(sheetBgChatterContainerXml, {
                    isInFormSheetBg: 'true',
                });
                setAttributes(chatterContainerHookXml, {
                    't-if': 'false',
                });
            }
        }

        return res;
    },
});
