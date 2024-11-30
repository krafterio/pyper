# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.models import Model
from ..tools.filestore import cleanup_filestore


class IrAttachment(Model):
    _inherit = 'ir.attachment'

    def _run_cleanup_filestore(self):
        cleanup_filestore(self.env)
