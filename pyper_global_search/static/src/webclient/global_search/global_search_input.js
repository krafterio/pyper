/* @odoo-module */

import {Component, useRef} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';

export class GlobalSearchInput extends Component {
    static template = 'pyper_global_search.GlobalSearchInput';

    static props = {
        className: {
            type: String,
            optional: true,
        },
        debounceDelay: {
            type: [Number, Boolean],
            optional: true,
        },
        openOnFocus: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        debounceDelay: 350,
        openOnFocus: false,
    };

    setup() {
        this.command = useService('command');
        this.inputRef = useRef('input');
        this.compositionStart = false;

        if (this.props.debounceDelay) {
            this._onInputSearch = debounce(this._onInputSearch, this.props.debounceDelay, false);
        }
    }

    get classes() {
        return {
            'o-global-search-input': true,
            ...(this.props.className || '').split(' ').reduce((obj, cls) => ({...obj, [cls]: true}), {}),
        };
    }

    _onClick() {
        if (this.props.openOnFocus) {
            this._openPalette();
        } else {
            this.inputRef.el?.focus();
        }
    }

    _onInputSearch() {
        this._openPalette();
    }

    _openPalette() {
        const onClose = () => {};
        const searchValue = this.compositionStart ? '>' : `>${this.inputRef.el.value.trim()}`;
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
