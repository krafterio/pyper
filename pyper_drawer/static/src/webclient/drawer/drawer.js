/** @odoo-module **/

import {
    Component,
    onMounted,
    onWillDestroy,
    useRef,
    useState,
    useEffect,
    useExternalListener,
} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {useBus, useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {listenSizeChange, SIZES, utils as uiUtils} from '@web/core/ui/ui_service';
import {_t} from '@web/core/l10n/translation';
import {getTransform} from '@pyper/core/ui/css';


const drawerRegistry = registry.category('drawer');

export class Drawer extends Component {
    static template = 'pyper_drawer.Drawer';

    static components = {
        DropdownItem: DropdownItem,
    };

    static props = {
        showRootApp: {
            type: Boolean,
            optional: true,
        },
        fixedTop: {
            type: Boolean,
            optional: true,
        },
        alwaysHeader: {
            type: Boolean,
            optional: true,
        },
        alwaysFooter: {
            type: Boolean,
            optional: true,
        },
        minifiable: {
            type: Boolean,
            optional: true,
        },
        initMinified: {
            type: Boolean,
            optional: true,
        },
        closeAction: {
            type: Boolean,
            optional: true,
        },
        dragEndRatio: {
            type: Number,
            optional: true,
        },
        hideEmptyCategory: {
            type: Boolean,
            optional: true,
        },
        hideCategoryLabelMinified: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        showRootApp: false,
        fixedTop: false,
        alwaysHeader: false,
        alwaysFooter: false,
        minifiable: false,
        initMinified: false,
        closeAction: false,
        dragEndRatio: 0.25,
        hideEmptyCategory: false,
        hideCategoryLabelMinified: false,
    };

    setup() {
        this.drawerService = useService('drawer');
        this.menuService = useService('menu');
        this.root = useRef('root');
        this.appSubMenus = useRef('appSubMenus');
        this.dragScrollables = undefined;
        this.dragScrolling = undefined;
        this.dragStartX = undefined;
        this.dragStartPosition = undefined;
        this.dragMaxWidth = undefined;
        this.dragDistance = 0;
        this.state = useState({
            opened: false,
            locked: this.drawerService.restoreLocked(),
            mini: this.drawerService.restoreMinified(this.props.initMinified),
            dragging: false,
            mounted: false,
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

        useBus(this.env.bus, 'MENUS:APP-CHANGED', renderAndAdapt);
        useBus(this.env.bus, 'DRAWER:TOGGLE', this.toggle);

        onMounted(() => {
            this.state.mounted = true;
            drawerRegistry.add('locked', this.isLocked, {force: true});
            drawerRegistry.add('mini', this.isMinified, {force: true});
        });

        useEffect(
            () => {
                this.adapt().then();
            },
            () => [adaptCounter]
        );

        listenSizeChange(() => {
            drawerRegistry.add('locked', this.isLocked, {force: true});
            drawerRegistry.add('mini', this.isMinified, {force: true});
        });
    }

    get classes() {
        return {
            'o_drawer': true,
            'o_drawer--ready': this.state.mounted,
            'o_drawer--opened': this.isOpened,
            'o_drawer--locked': this.isLocked,
            'o_drawer--mini': this.isMinified,
            'o_drawer--fixed-top': this.isFixedTop,
            'o_drawer--hoverable': this.isHoverable,
            'o_drawer--dragging': this.isDragging,
        };
    }

    get isSmallScreen() {
        return uiUtils.getSize() <= SIZES.LG;
    }

    get isLocked() {
        return this.state.locked && !this.isSmallScreen;
    }

    get isMinifiable() {
        return this.props.minifiable;
    }

    get isMinified() {
        return this.state.mini && !this.isSmallScreen;
    }

    get isHoverable() {
        return this.isSmallScreen || !this.state.locked;
    }

    get isDraggable() {
        return this.isHoverable;
    }

    get isDragging() {
        return this.state.dragging;
    }

    get isOpened() {
        return this.state.opened;
    }

    get isClosed() {
        return !this.state.opened;
    }

    get isFixedTop() {
        return this.props.fixedTop && !this.isSmallScreen;
    }

    get displayCategoryName() {
        return !this.isMinified || (this.isMinified && !this.props.hideCategoryLabelMinified)
    }

    get displayHeader() {
        return this.isSmallScreen || this.props.alwaysHeader;
    }

    get displayFooter() {
        return this.isSmallScreen || this.props.alwaysFooter;
    }

    get currentApp() {
        return this.menuService.getCurrentApp();
    }

    get currentAppSections() {
        const currentId = this.currentApp && !this.props.showRootApp ? this.currentApp.id : 'root';
        const menu = this.menuService.getMenuAsTree(currentId);

        return menu.childrenTree || [];
    }

    get currentCategoryAppSections() {
        const categories = {};

        this.currentAppSections.forEach((menu) => {
            if (undefined === categories[menu.category]) {
                categories[menu.category] = {
                    display_name: menu.category_display_name || _t('Other'),
                    value: menu.category || 'other',
                    menus: [],
                }
            }

            categories[menu.category]['menus'].push(menu);
        });

        if (this.props.hideEmptyCategory) {
            delete categories[undefined];
        }

        return categories;
    }

    open() {
        if (this.isSmallScreen) {
            if (!this.isOpened) {
                this.state.opened = true;
                this.root.el.style.transform = '';
            }
        } else {
            if (this.isLocked && this.isMinifiable && this.isMinified) {
                this.state.mini = false;
            } else if (this.isLocked && this.isMinifiable && !this.isMinified) {
                // Nothing do
            } else if (this.isLocked && !this.isMinifiable && this.isMinified) {
                this.state.mini = false;
            } else if (this.isLocked && !this.isMinifiable && !this.isMinified) {
                // Nothing do
            } else if (!this.isLocked && this.isMinifiable && this.isMinified) {
                this.state.locked = true;
            } else if (!this.isLocked && this.isMinifiable && !this.isMinified) {
                this.state.locked = true;
            } else if (!this.isLocked && !this.isMinifiable && this.isMinified) {
                this.state.locked = true;
                this.state.mini = false;
            } else if (!this.isLocked && !this.isMinifiable && !this.isMinified) {
                this.state.locked = true;
            }

            this.root.el.style.transform = '';
            drawerRegistry.add('locked', this.isLocked, {force: true});
            drawerRegistry.add('mini', this.isMinified, {force: true});
            this.drawerService.saveLocked(this.state.locked);
            this.drawerService.saveMinified(this.state.mini);

            debounce(() => window.dispatchEvent(new CustomEvent('resize')), 1)();
        }
    }

    close() {
        if (this.isSmallScreen) {
            if (this.isOpened) {
                this.state.opened = false;
                this.root.el.style.transform = '';
            }
        } else {
            if (this.isLocked && this.isMinifiable && this.isMinified) {
                // Nothing do
            } else if (this.isLocked && this.isMinifiable && !this.isMinified) {
                this.state.mini = true;
            } else if (this.isLocked && !this.isMinifiable && this.isMinified) {
                this.state.mini = false;
            } else if (this.isLocked && !this.isMinifiable && !this.isMinified) {
                this.state.locked = false;
            } else if (!this.isLocked && this.isMinifiable && this.isMinified) {
                this.state.mini = false;
            } else if (!this.isLocked && this.isMinifiable && !this.isMinified) {
                // Nothing do
            } else if (!this.isLocked && !this.isMinifiable && this.isMinified) {
                this.state.mini = false;
            } else if (!this.isLocked && !this.isMinifiable && !this.isMinified) {
                // Nothing do
            }

            this.root.el.style.transform = '';
            drawerRegistry.add('locked', this.isLocked, {force: true});
            drawerRegistry.add('mini', this.isMinified, {force: true});
            this.drawerService.saveLocked(this.state.locked);
            this.drawerService.saveMinified(this.state.mini);

            debounce(() => window.dispatchEvent(new CustomEvent('resize')), 1)();
        }
    }

    toggle() {
        if (this.isSmallScreen) {
            if (this.isOpened) {
                this.close();
            } else {
                this.open();
            }
        } else {
            if (this.isLocked && this.isMinifiable && this.isMinified) {
                this.open();
            } else if (this.isLocked && this.isMinifiable && !this.isMinified) {
                this.close();
            } else if (this.isLocked && !this.isMinifiable && this.isMinified) {
                this.open();
            } else if (this.isLocked && !this.isMinifiable && !this.isMinified) {
                this.close();
            } else if (!this.isLocked && this.isMinifiable && this.isMinified) {
                this.open();
            } else if (!this.isLocked && this.isMinifiable && !this.isMinified) {
                this.open();
            } else if (!this.isLocked && !this.isMinifiable && this.isMinified) {
                this.open();
            } else if (!this.isLocked && !this.isMinifiable && !this.isMinified) {
                this.open();
            }
        }
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

    onNavBarDropdownItemSelection(menu) {
        if (menu) {
            this.menuService.selectMenu(menu);
        }
    }

    getMenuItemHref(payload) {
        const parts = [`menu_id=${payload.id}`];

        if (payload.actionID) {
            parts.push(`action=${payload.actionID}`);
        }

        return '#' + parts.join('&');
    }

    _onTouchStartDrag(ev) {
        if (!this.isDraggable) {
            return;
        }

        this.dragScrollables = ev
            .composedPath()
            .filter(
                (e) => {
                    const valid = e.nodeType === 1
                        && (this.root.el.contains(e) || e === this.root.el)
                        && e.scrollHeight > e.getBoundingClientRect().height
                        && ['auto', 'scroll'].includes(window.getComputedStyle(e)['overflow-y']);

                    if (valid) {
                        e.addEventListener('scroll', this._onTouchScroll.bind(this));
                    }

                    return valid;
                }
            );

        this.state.dragging = true;
        this.dragStartX = ev.touches[0].clientX;
        this.dragStartPosition = getTransform(this.root.el, true).e;
        this.dragMaxWidth = this.root.el.getBoundingClientRect().width;
        this.dragDistance = 0;
        this.root.el.style.transition = 'none';
    }

    /**
     * @private
     * @param {TouchEvent} ev
     */
    _onTouchMoveDrag(ev) {
        if (!this.isDraggable || !this.isDragging) {
            return;
        }

        this.dragDistance = Math.round(ev.touches[0].clientX - this.dragStartX);
        let translateX = this.dragStartPosition + this.dragDistance;
        translateX = Math.max(translateX, -this.dragMaxWidth);
        translateX = Math.min(translateX, 0);

        if (this.dragScrolling) {
            return;
        }

        this.root.el.style.transform = `translateX(${translateX}px)`;
    }

    /**
     * @private
     * @param {TouchEvent} ev
     */
    _onTouchEndDrag(ev) {
        if (!this.isDraggable || !this.isDragging) {
            return;
        }

        this.dragScrollables.forEach((e) => {
            e.removeEventListener('scroll', this._onTouchScroll.bind(this));
        });

        const dragDistance = this.dragDistance;
        const dragMaxWidth = this.dragMaxWidth;
        const dragActionable = !this.dragScrolling;

        this.state.dragging = false;
        this.dragScrollables = undefined;
        this.dragScrolling = undefined;
        this.dragStartX = undefined;
        this.dragStartPosition = undefined;
        this.dragMaxWidth = undefined;
        this.dragDistance = 0;
        this.root.el.style.transition = '';

        if (dragActionable && Math.abs(dragDistance) >= (dragMaxWidth * this.props.dragEndRatio)) {
            if (this.isOpened) {
                this.close();
            } else if (this.isClosed) {
                this.open();
            }
        }

        this.root.el.style.transform = '';
    }

    _onTouchScroll() {
        this.dragScrolling = true;
    }
}
