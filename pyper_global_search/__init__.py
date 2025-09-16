# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from . import controllers
from . import models


def post_init_hook(env):
    env['ir.global_search.model'].sudo()._update_search_models()
