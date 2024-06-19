# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

from . import models

def activate_variant_on_install(env):
    env['res.config.settings'].create({
        'group_product_variant': True,  # Activate variant
    }).execute()
