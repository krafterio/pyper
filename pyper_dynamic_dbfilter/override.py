# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

import logging
import re

from odoo import http
from odoo.tools import config

db_filter_origin = http.db_filter


def db_filter(dbs, host=None):
    db_filter_header = http.request.httprequest.environ.get('HTTP_X_PYPER_DB_FILTER')

    if db_filter_header:
        return [db for db in dbs if re.match(db_filter_header, db)]

    return db_filter_origin(dbs, host)


if config.get('proxy_mode') and 'pyper_dynamic_dbfilter' in config.get('server_wide_modules'):
    logging.getLogger(__name__).info('Pyper HTTP Dynamic DB Filter enabled')
    http.db_filter = db_filter
