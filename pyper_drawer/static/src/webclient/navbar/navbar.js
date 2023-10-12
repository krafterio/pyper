/** @odoo-module **/

import {Drawer} from '../drawer/drawer';
import {DrawerAppMenu} from '../drawer/drawer_app_menu';
import {DrawerToggler} from '../drawer/drawer_toggler';
import {NavBar} from '@web/webclient/navbar/navbar';

NavBar.components.Drawer = Drawer;
NavBar.components.DrawerAppMenu = DrawerAppMenu;
NavBar.components.DrawerToggler = DrawerToggler;
