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
import {_t} from '@web/core/l10n/translation';
import {debounce} from '@web/core/utils/timing';


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
        hideCategoryLabel: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        showRootApp: false,
        hideEmptyCategory: false,
        hideCategoryLabel: false,
    };

    setup() {
        this.overlayMenuService = useState(useService('overlay_menu'));
        this.menuService = useService('menu');
        this.root = useRef('root');
        this.appSubMenus = useRef('appSubMenus');

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

    get displayCategoryName() {
        return !this.props.hideCategoryLabel;
    }

    get isOpened() {
        return this.overlayMenuService.isOpened;
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
        }
    }

    close() {
        if (this.overlayMenuService.isOpened) {
            this.overlayMenuService.opened = false;
        }
    }

    toggle() {
        if (this.overlayMenuService.isClosed) {
            this.open();
        } else {
            this.close();
        }
    }

    onItemSelection(menu) {
        this.overlayMenuService.selectMenu(menu);
    }
}
