/* @odoo-module */

import {Component, useRef} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';

export class GlobalSearchInput extends Component {
    static template = 'pyper_global_search.GlobalSearchInput';

    static props = {
        className: {
            type: String,
            optional: true,
        },
        minified: {
            type: Boolean,
            optional: true,
        },
        debounceDelay: {
            type: [Number, Boolean],
            optional: true,
        },
        openOnEnter: {
            type: Boolean,
            optional: true,
        },
        openOnFocus: {
            type: Boolean,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    };

    static defaultProps = {
        debounceDelay: 350,
        minified: false,
        openOnEnter: false,
        openOnFocus: false,
    };

    setup() {
        this.command = useService('command');
        this.inputRef = useRef('input');
        this.compositionStart = false;

        if (!this.props.openOnEnter && this.props.debounceDelay) {
            this._onInputSearch = debounce(this._onInputSearch, this.props.debounceDelay, false);
        }
    }

    get classes() {
        return {
            'o-global-search-input': true,
            ...(this.props.className || '').split(' ').reduce((obj, cls) => ({...obj, [cls]: true}), {}),
        };
    }

    get placeholder() {
        return _t('Quick search');
    }

    get hotkey() {
        return 'g';
    }

    _onKeyup(e) {
        if (this.props.openOnEnter && e.key === 'Enter' && this.inputRef.el?.value) {
            this._openPalette();
        }
    }

    _onClick() {
        if (this.props.openOnFocus || this.props.minified) {
            this._openPalette();
        } else {
            this.inputRef.el?.focus();
        }
    }

    _onInputSearch() {
        if (!this.props.openOnEnter) {
            this._openPalette();
        }
    }

    _openPalette() {
        const onClose = () => {};
        const searchValue = this.compositionStart ? '>' : `>${this.inputRef.el?.value.trim() || ''}`;
        this.command.openMainPalette({searchValue}, onClose);
    }

    _onInputBlur() {
        this.inputRef.el.value = '';
        this.compositionStart = false;
    }

    _onCompositionStart() {
        this.compositionStart = true;
    }
}
