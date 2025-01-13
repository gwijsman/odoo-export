#
# OdooProductFinder
#
# Gert Wijsman
# January 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooProduct import OdooProduct

logger = logging.getLogger(__name__)

class OdooProductFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'product'
        self.name = 'Product'
        self.setup_target_products()

    def get_product_id_for_id(self, oid):
        op = OdooProduct(self.odoo_in_info, oid)  
        name = op.data()['name']
        nid = op.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(op)
        return nid
    
    def retrieve_new_id(self, product):
        product_name = product.data()['name']
        domain = [[['name', '=', product_name]]]
        new_products = self.odoo_out_info.kw_search_result('product.product', domain)
        if len(new_products) == 0:
            logger.warning("No product found for %s", product_name)
            return False 
        elif len(new_products) > 1:
            logger.warning("More products found for %s", product_name)
        nid = new_products[0]
        product.data()['toid2025'] = nid
        product.set_cached_record()
        return nid 

    def setup_target_products(self):
        relevant = [
            [3,   'M&S Diagnostics'], 
            [80,  'M&S SWEG'], 
            [82,  'M&S Water Office'], 
            [81,  'M&S Realworld Modules'], 
            [2,   'Diagnostics License'],
            [97,  'SWEG License'], 
            [95,  'Water Office License'], 
            [247, 'Services Water Office'], 
            [114, 'Services Diagnostics'], 
            [246, 'Services SWEG'],
        ]
        for item in relevant:
            oid = item[0]
            nname = item[1]
            op = OdooProduct(self.odoo_in_info, oid)  
            op.data()['name'] = nname
            nid = op.sqlite_to_id()
            if nid is False:
                nid = self.retrieve_new_id(op)
            if nid is False:
                nid = op.write_to_database(self.odoo_out_info)
                op.data()['toid2025'] = nid
                op.set_cached_record()
                logger.warning("Setup New product for %s", nname) 

    def get_migration_product(self):
        return self.get_product_id_for_id(999)