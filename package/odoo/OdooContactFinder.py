#
# OdooContactFinder
#
# Gert Wijsman
# Januari 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooContact import OdooContact

logger = logging.getLogger(__name__)

class OdooContactFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'contact'
        self.name = 'Contact'

    def get_contact_id_for_id(self, oid):
        op = OdooContact(self.odoo_in_info, oid)  
        name = op.data()['name']
        nid = op.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(op)
        return nid
    
    def retrieve_new_id(self, contact):
        contact_name = contact.data()['name']
        domain = [[['name', '=', contact_name]]]
        new_contacts = self.odoo_out_info.kw_search_result('res.partner', domain)
        if len(new_contacts) == 0:
            logger.warning("No contact found for %s", contact_name)
            return False 
        elif len(new_contacts) > 1:
            logger.warning("More contacts found for %s", contact_name)
        nid = new_contacts[0]
        contact.data()['toid2025'] = nid
        contact.set_cached_record()
        return nid 
