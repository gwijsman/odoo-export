#
# OdooCategoryFinder
#
# Gert Wijsman
# January 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooCategory import OdooCategory

logger = logging.getLogger(__name__)

class OdooCategoryFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'category'
        self.name = 'Category'
        self.setup_target_categories()

    def get_category_id_for_id(self, oid):
        oc = OdooCategory(self.odoo_in_info, oid)  
        name = oc.data()['name']
        nid = oc.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(oc)
        return nid
    
    def retrieve_new_id(self, category):
        category_name = category.data()['name']
        domain = [[['name', '=', category_name]]]
        new_categories = self.odoo_out_info.kw_search_result('res.partner.category', domain)
        if len(new_categories) == 0:
            logger.warning("No category found for %s", category_name)
            return False 
        elif len(new_categories) > 1:
            logger.warning("More categories found for %s", category_name)
        nid = new_categories[0]
        category.data()['toid2025'] = nid
        category.set_cached_record()
        return nid 

    def setup_target_categories(self):
        relevant_tags = [48,49,64,18,65,44,45,46,17,55,9,25,53]
        for tag in relevant_tags:
            if self.get_category_id_for_id(tag) is False:
                oc = OdooCategory(self.odoo_in_info, tag)  
                name = oc.data()['name']
                oc.write_to_database(self.odoo_out_info)
        new_tags = {999: 'ODOO 2025'}
        for oid, tag in new_tags.items():
            oc = OdooCategory(self.odoo_in_info, oid, tag)  
            name = oc.data()['name']
            nid = oc.sqlite_to_id()
            if nid is False:
                nid = oc.write_to_database(self.odoo_out_info)
            oc.data()['toid2025'] = nid
            oc.set_cached_record()

    def get_migration_category(self):
        return self.get_category_id_for_id(999)