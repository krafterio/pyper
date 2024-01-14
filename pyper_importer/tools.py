# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from typing import Any


def property_path(data: dict, path: str, default=False) -> Any:
    paths = path.split('.')
    value = data

    for key in paths:
        if key in value:
            value = value[key]
        else:
            return default

    return value
