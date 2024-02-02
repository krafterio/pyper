from odoo import models
from odoo.tools.safe_eval import safe_eval

class Model(models.AbstractModel):
    _inherit = 'ir.ui.view'

    def _postprocess_access_rights(self, tree):
        """
        Allow setting element as "readonly" instead of removing it upon access failure 
        """
        # TODO: Setup real attributes with RelaxNG instead of passing through options attribute
        for node in tree.xpath('//*[@groups and @options]'):
            # TODO: Allow multiple actions
            attrib_groups = node.attrib.pop('groups')
            if attrib_groups and not self.user_has_groups(attrib_groups):
                attrib_group_action = node.attrib.get('options') \
                    and safe_eval(node.attrib.get('options')).get('group_action')
                if attrib_group_action == 'readonly':
                    node.set('readonly', 'True')
                else:
                    node.getparent().remove(node)
        return super()._postprocess_access_rights(tree)