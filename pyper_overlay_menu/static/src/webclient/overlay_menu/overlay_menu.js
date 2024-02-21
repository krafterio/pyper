/** @odoo-module **/

import {
    Component,
    onMounted,
    onWillDestroy,
    useEffect,
    useExternalListener,
    useRef,
    useState,
} from '@odoo/owl';
import {useBus, useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';
import {isMobileOS} from '@web/core/browser/feature_detection';
import {useHotkey} from '@web/core/hotkeys/hotkey_hook';
import {OverlayFooter} from './overlay_footer';


export class OverlayMenu extends Component {
    static template = 'pyper_overlay_menu.OverlayMenu';

    static props = {
        showRootApp: {
            type: Boolean,
            optional: true,
        },
        hideEmptyCategory: {
            type: Boolean,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    };

    static defaultProps = {
        showRootApp: false,
        hideEmptyCategory: false,
    };

    setup() {
        this.overlayMenuService = useState(useService('overlay_menu'));
        this.menuService = useService('menu');
        this.command = useService('command');
        this.ui = useService('ui');
        this.root = useRef('root');
        this.appSubMenus = useRef('appSubMenus');
        this.inputRef = useRef('input');
        this.compositionStart = false;

        this.state = useState({
            focusedIndex: null,
        });

        const debouncedAdapt = debounce(this.adapt.bind(this), 250);
        onWillDestroy(() => {
            debouncedAdapt.cancel();
        });
        useExternalListener(window, 'resize', debouncedAdapt);

        let adaptCounter = 0;
        const renderAndAdapt = () => {
            adaptCounter++;
            this.render();
        };

        if (!this.env.isSmall) {
            this._registerHotkeys();
        }

        useBus(this.env.bus, 'MENUS:APP-CHANGED', renderAndAdapt);
        useBus(this.env.bus, 'OVERLAY-MENU:TOGGLE', this.toggle);
        useBus(this.env.bus, 'OVERLAY-MENU:SELECT-MENU', (evt) => {
            this.selectMenu(evt.detail);
        });

        onMounted(() => {
            this.overlayMenuService.mounted = true;
        });

        useEffect(
            () => {
                this.adapt().then();
            },
            () => [adaptCounter]
        );
    }

    get classes() {
        return {
            'o_overlay_menu': true,
            'o_overlay_menu--ready': this.overlayMenuService.mounted,
            'o_overlay_menu--opened': this.overlayMenuService.isOpened,
        };
    }

    get currentApp() {
        return this.menuService.getCurrentApp();
    }

    get currentAppSections() {
        const currentId = this.currentApp && !this.props.showRootApp ? this.currentApp.id : 'root';
        const menu = this.menuService.getMenuAsTree(currentId);

        return menu.childrenTree || [];
    }

    get currentFilteredAppSections() {
        const apps = [];

        this.currentAppSections.forEach((menu) => {
            if (this.props.hideEmptyCategory) {
                if (menu.category) {
                    apps.push(menu);
                }
            } else {
                apps.push(menu);
            }
        });

        return apps;
    }

    get isOpened() {
        return this.overlayMenuService.isOpened;
    }

    get maxLineItemNumber() {
        const items = this.appSubMenus.el ? this.appSubMenus.el.children : [];
        let countItemPerLine = 0;
        let firstTop = undefined;

        for (let i = 0; i < items.length; ++i) {
            const rect = items[i].getBoundingClientRect();

            if (firstTop === undefined) {
                firstTop = rect.top;
            }

            if (rect.top > firstTop) {
                break;
            } else {
                countItemPerLine++;
            }
        }

        return countItemPerLine;
    }

    async adapt() {
        if (!this.root.el) {
            // currently, the promise returned by 'render' is resolved at the end of
            // the rendering even if the component has been destroyed meanwhile, so we
            // may get here and have this.el unset
            return;
        }

        // ------- Initialize -------
        // Get the sectionsMenu
        const sectionsMenu = this.appSubMenus.el;
        if (!sectionsMenu) {
            // No need to continue adaptations if there is no sections menu.
            return;
        }

        return this.render();
    }

    selectMenu(menu) {
        if (menu) {
            this.menuService.selectMenu(menu).then();
            this.close();
        }
    }

    open() {
        if (this.overlayMenuService.isClosed) {
            this.overlayMenuService.opened = true;

            debounce(() => {
                if (!isMobileOS()) {
                    this._focusInput();
                }
            }, 0)();
        }
    }

    close() {
        if (this.overlayMenuService.isOpened) {
            this.overlayMenuService.opened = false;
            this._focusInput();
            this.inputRef.el.value = '';
            this.state.focusedIndex = null;
        }
    }

    toggle() {
        if (this.overlayMenuService.isClosed) {
            this.open();
        } else {
            this.close();
        }
    }

    _registerHotkeys() {
        const hotkeys = [
            ['ArrowDown', () => this._updateFocusedIndex('nextLine')],
            ['ArrowRight', () => this._updateFocusedIndex('nextColumn')],
            ['ArrowUp', () => this._updateFocusedIndex('previousLine')],
            ['ArrowLeft', () => this._updateFocusedIndex('previousColumn')],
            ['Tab', () => this._updateFocusedIndex('nextElem')],
            ['shift+Tab', () => this._updateFocusedIndex('previousElem')],
            [
                'Enter',
                () => {
                    const menu = this.currentFilteredAppSections[this.state.focusedIndex];

                    if (menu) {
                        this.selectMenu(menu);
                    }
                },
            ],
            ['Escape', () => this.close()],
        ];

        hotkeys.forEach((hotkey) => {
            useHotkey(...hotkey, {
                allowRepeat: true,
            });
        });

        useExternalListener(window, 'keydown', this._onKeydownFocusInput);
    }

    _onKeydownFocusInput() {
        if (
            document.activeElement !== this.inputRef.el
            && this.ui.activeElement === document
            && !['TEXTAREA', 'INPUT'].includes(document.activeElement.tagName)
        ) {
            this._focusInput();
        }
    }

    /**
     * Update this.state.focusedIndex if not null.
     *
     * @private
     * @param {string} cmd
     */
    _updateFocusedIndex(cmd) {
        const nbrApps = this.currentFilteredAppSections.length;
        const lastIndex = nbrApps - 1;
        const focusedIndex = this.state.focusedIndex;

        if (lastIndex < 0) {
            return;
        }

        if (focusedIndex === null) {
            this.state.focusedIndex = 0;

            return;
        }

        const lineNumber = Math.ceil(nbrApps / this.maxLineItemNumber);
        const currentLine = Math.ceil((focusedIndex + 1) / this.maxLineItemNumber);
        let newIndex = undefined;

        switch (cmd) {
            case 'previousElem':
                newIndex = focusedIndex - 1;
                break;
            case 'nextElem':
                newIndex = focusedIndex + 1;
                break;
            case 'previousColumn':
                if (focusedIndex % this.maxLineItemNumber) {
                    // App is not the first one on its line
                    newIndex = focusedIndex - 1;
                } else {
                    newIndex = focusedIndex + Math.min(lastIndex - focusedIndex, this.maxLineItemNumber - 1);
                }

                break;
            case 'nextColumn':
                if (focusedIndex === lastIndex || (focusedIndex + 1) % this.maxLineItemNumber === 0) {
                    // App is the last one on its line
                    newIndex = (currentLine - 1) * this.maxLineItemNumber;
                } else {
                    newIndex = focusedIndex + 1;
                }

                break;
            case 'previousLine':
                if (currentLine === 1) {
                    newIndex = focusedIndex + (lineNumber - 1) * this.maxLineItemNumber;

                    if (newIndex > lastIndex) {
                        newIndex = lastIndex;
                    }
                } else {
                    // Go to the previous line on same column
                    newIndex = focusedIndex - this.maxLineItemNumber;
                }

                break;
            case 'nextLine':
                if (currentLine === lineNumber) {
                    newIndex = focusedIndex % this.maxLineItemNumber;
                } else {
                    // Go to the next line on the closest column
                    newIndex = focusedIndex + Math.min(this.maxLineItemNumber, lastIndex - focusedIndex);
                }

                break;
        }

        if (newIndex < 0) {
            newIndex = lastIndex;
        } else if (newIndex > lastIndex) {
            newIndex = 0;
        }

        this.state.focusedIndex = newIndex;
    }

    _focusInput() {
        if (!this.env.isSmall && this.inputRef.el) {
            this.inputRef.el.focus({preventScroll: true});
        }
    }

    _onInputSearch() {
        const onClose = () => {
            this.close();
        };
        const searchValue = this.compositionStart ? '/' : `/${this.inputRef.el.value.trim()}`;
        this.compositionStart = false;
        this.command.openMainPalette({searchValue, FooterComponent: OverlayFooter}, onClose);
    }

    _onInputBlur() {
        if (isMobileOS()) {
            return;
        }

        setTimeout(() => {
            if (document.activeElement === document.body && this.ui.activeElement === document) {
                this._focusInput();
            }
        }, 0);
    }

    _onCompositionStart() {
        this.compositionStart = true;
    }
}
