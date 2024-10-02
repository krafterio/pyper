# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models


def _create_drop_contact_endpoint_config_param(env):
    env['ir.config_parameter'].set_param('pyper_drop_contact_connector.endpoint_api', 'https://api.dropcontact.io')
