#
# OdooTitleFinder
#
# Gert Wijsman
# January 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooTitle import OdooTitle

logger = logging.getLogger(__name__)

class OdooTitleFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'title'
        self.name = 'Title'
#        self.setup_target_title()

    def get_title_id_for_id(self, oid):
        oc = OdooTitle(self.odoo_in_info, oid)  
        name = oc.data()['name']
        nid = oc.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(oc)
        return nid
    
    def retrieve_new_id(self, title):
        title_name = title.data()['name']
        domain = [[['name', '=', title_name]]]
        new_title = self.odoo_out_info.kw_search_result('res.partner.title', domain)
        if len(new_title) == 0:
            logger.warning("No title found for %s", title_name)
            return False 
        elif len(new_title) > 1:
            logger.warning("More Titles found for %s", title_name)
        nid = new_title[0]
        title.data()['toid2025'] = nid
        title.set_cached_record()
        return nid 

#    def setup_target_title(self):
#        relevant_tags = [48,49,64,18,65,44,45,46,17,55,9,25,53]
#        for tag in relevant_tags:
#            if self.get_title_id_for_id(tag) is False:
#                oc = OdooTitle(self.odoo_in_info, tag)  
#                name = oc.data()['name']
#                oc.write_to_database(self.odoo_out_info)

