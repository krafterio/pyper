# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import models
from odoo.api import Environment


def serialize(value):
    if isinstance(value, models.BaseModel):
        return {'_model': value._name, '_ids': value.ids}
    elif isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [serialize(v) for v in value]
    elif isinstance(value, tuple):
        return [serialize(v) for v in value]

    return value


def deserialize(env: Environment, value):
    if isinstance(value, dict) and '_model' in value:
        return env[value['_model']].browse(value['_ids'])
    elif isinstance(value, dict):
        return {k: deserialize(env, v) for k, v in value.items()}
    elif isinstance(value, list):
        return [deserialize(env, v) for v in value]

    return value
