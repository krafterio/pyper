/** @odoo-module */

import {EditMenuDialog, MenuDialog} from '@website/components/dialog/edit_menu';

import {patch} from '@web/core/utils/patch';
import {useEffect, useState} from '@odoo/owl';

const useControlledInput = (initialValue, validate) => {
    const input = useState({
        value: initialValue,
        hasError: false,
    });

    const isValid = () => {
        if (validate(input.value)) {
            return true;
        }
        input.hasError = true;
        return false;
    };

    useEffect(() => {
        input.hasError = false;
    }, () => [input.value]);

    return {
        input,
        isValid,
    };
};

patch(MenuDialog.prototype, {
    setup() {
        super.setup();
        this.structuredMenuColumns = useControlledInput(this.props.structuredMenuColumns, value => !!value);
    },

    onClickOk() {
        if (this.name.isValid() && this.props.isStructuredMenu) {
            this.props.save(this.name.input.value, this.url.input.value, this.structuredMenuColumns.input.value);
            this.props.close();
        } else {
            super.onClickOk();
        }
    },
});

MenuDialog.props.isStructuredMenu = {type: Boolean, optional: true};
MenuDialog.props.structuredMenuColumns = {type: Number, optional: true};

patch(EditMenuDialog.prototype, {
    addStructuredMenu() {
        this.dialogs.add(MenuDialog, {
            isMegaMenu: true, // Only to hide fields
            isStructuredMenu: true,
            save: (name, url, isNewWindow) => {
                const newMenu = {
                    fields: {
                        id: `menu_${(new Date).toISOString()}`,
                        name,
                        url: '#',
                        new_window: isNewWindow,
                        'is_structured_menu': true,
                        sequence: 0,
                        'parent_id': false,
                    },
                    'children': [],
                };
                this.map.set(newMenu.fields['id'], newMenu);
                this.state.rootMenu.children.push(newMenu);
            },
        });
    },

    editMenu(id) {
        const menuToEdit = this.map.get(id);
        const isStructuredMenu = menuToEdit.fields['is_structured_menu']

        if (isStructuredMenu) {
            this.dialogs.add(MenuDialog, {
                name: menuToEdit.fields['name'],
                url: menuToEdit.fields['url'],
                isStructuredMenu: isStructuredMenu,
                structuredMenuColumns: menuToEdit.fields['structured_menu_columns'],
                save: (name, url, structuredMenuColumns) => {
                    menuToEdit.fields['name'] = name;
                    menuToEdit.fields['url'] = url;
                    menuToEdit.fields['structured_menu_columns'] = structuredMenuColumns
                },
            });
        } else {
            super.editMenu(id);
        }
    },

    _isAllowedMove(current, elementSelector) {
        // Allow move structured menu item only in root level
        if (current.element.dataset.isStructuredMenu === 'true') {
            return current.placeHolder.parentNode.closest(elementSelector) === null;
        }

        return super._isAllowedMove(current, elementSelector);
    },
});
