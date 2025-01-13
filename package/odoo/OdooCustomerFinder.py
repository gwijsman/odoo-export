#
# OdooCustomerFinder
#
# Gert Wijsman
# Januari 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooCustomer import OdooCustomer

logger = logging.getLogger(__name__)

class OdooCustomerFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'cusomter'
        self.name = 'Customer'

    def get_customer_id_for_id(self, oid):
        op = OdooCustomer(self.odoo_in_info, oid)  
        if op is False:
            return False
        name = op.data()['name']
        nid = op.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(op)
        return nid
    
    def retrieve_new_id(self, cusomter):
        customer_name = cusomter.data()['name']
        domain = [[['name', '=', customer_name]]]
        new_customers = self.odoo_out_info.kw_search_result('res.partner', domain)
        if len(new_customers) == 0:
            logger.warning("No cusomter found for %s", customer_name)
            return False 
        elif len(new_customers) > 1:
            logger.warning("More partners found for %s", customer_name)
        nid = new_customers[0]
        cusomter.data()['toid2025'] = nid
        cusomter.set_cached_record()
        return nid 
