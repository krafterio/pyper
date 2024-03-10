# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import ast
import copy
import logging
import os

from odoo import modules, tools
from odoo.tools import config

_logger = logging.getLogger(__name__)
_original_module_get_modules = modules.module.get_modules
_original_load_manifest = modules.module.load_manifest


class PyperSaas:
    _DEFAULT_PYPER = {
        'enable': None,
        'include_self_addons': False,
        'include_minimal_addons': True,
        'available_addons': [],
        'uninstallable_addons': [],
    }

    _MINIMAL_AVAILABLE_ADDONS = [
        'auth_totp',
        'base',
        'base_automation',
        'base_import',
        'base_setup',
        'bus',
        'iap',
        'iap_mail',
        'mail',
        'phone_validation',
        'resource',
        'sms',
        'web',
        'web_editor',
        'web_tour',
    ]

    _MINIMAL_UNINSTALLABLE_ADDONS = [
        'hr_timesheet',
        'mass_mailing',
        'mrp',
        'project',
        'sales_team',
        'stock',
        'website',
    ]

    def __init__(self, addons_path: list[str]):
        pyper = copy.deepcopy(PyperSaas._DEFAULT_PYPER)

        for addon_path in addons_path:
            pyper_file = addon_path + '/__pyper_saas__.py'

            if os.path.isfile(pyper_file):
                with tools.file_open(pyper_file, mode='r') as f:
                    p_pyper = ast.literal_eval(f.read())

                    if p_pyper.get('include_self_addons', False):
                        p_available_addons = list(p_pyper.get('available_addons', []))

                        for sub_addon in os.listdir(addon_path):
                            sub_addon_manifest = addon_path + '/' + sub_addon + '/__manifest__.py'

                            if os.path.isfile(sub_addon_manifest) and sub_addon not in p_available_addons:
                                p_available_addons.append(sub_addon)

                        p_pyper.update({'available_addons': p_available_addons})

                    pyper.update(PyperSaas._merge(pyper, p_pyper))

        if pyper.get('enable', None) is None:
            pyper.update({'enable': len(pyper.get('available_addons', [])) > 0})

        self.enable = pyper.get('enable', False)
        self.available_addons = PyperSaas._get_available_addons(pyper)
        self.uninstallable_addons = PyperSaas._get_uninstallable_addons(pyper)

    def is_loadable_module(self, module):
        return module in self.available_addons or module in self.uninstallable_addons

    def is_uninstallable_module(self, module):
        return module in self.uninstallable_addons

    @staticmethod
    def _get_available_addons(pyper: dict):
        available_addons = []

        if pyper.get('include_minimal_addons', True):
            for min_addon in PyperSaas._MINIMAL_AVAILABLE_ADDONS:
                available_addons.append(min_addon)

        for p_addon in pyper.get('available_addons', []):
            if p_addon not in available_addons:
                available_addons.append(p_addon)

        return available_addons

    @staticmethod
    def _get_uninstallable_addons(pyper: dict):
        uninstallable_addons = []

        if pyper.get('include_minimal_addons', True):
            for min_addon in PyperSaas._MINIMAL_UNINSTALLABLE_ADDONS:
                uninstallable_addons.append(min_addon)

        for p_addon in pyper.get('uninstallable_addons', []):
            if p_addon not in uninstallable_addons:
                uninstallable_addons.append(p_addon)

        return uninstallable_addons

    @staticmethod
    def _merge(destination, source):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                PyperSaas._merge(node, value)
            elif isinstance(value, list):
                node = destination.setdefault(key, [])

                for val in value:
                    if val not in node:
                        node.append(val)
            else:
                destination[key] = value

        return destination


def _overload_module_get_modules(pyper: PyperSaas):
    loadable_modules = _original_module_get_modules()
    validated_modules = []

    if pyper.enable and (pyper.available_addons or pyper.uninstallable_addons):
        for module in loadable_modules:
            if pyper.is_loadable_module(module) and module not in validated_modules:
                validated_modules.append(module)
    else:
        validated_modules = loadable_modules

    validated_modules.sort()

    return validated_modules


def _overload_load_manifest(pyper: PyperSaas, module, mod_path=None):
    res = _original_load_manifest(module, mod_path=mod_path)
    installable = res.get('installable', False)

    if installable and pyper.is_uninstallable_module(module):
        res['installable'] = False
        res['to_buy'] = True

    return res


def post_load():
    _logger.info('Applying module patches for SaaS...')

    pyper = PyperSaas(config.get('addons_path', '').strip().split(','))

    def __overload_module_get_modules():
        return _overload_module_get_modules(pyper)

    def __overload_load_manifest(module, mod_path=None):
        return _overload_load_manifest(pyper, module, mod_path=mod_path)

    # Overload get_modules
    modules.module.get_modules = __overload_module_get_modules
    modules.get_modules = __overload_module_get_modules
    # Overload load_manifest
    modules.module.load_manifest = __overload_load_manifest
    modules.load_manifest = __overload_load_manifest
