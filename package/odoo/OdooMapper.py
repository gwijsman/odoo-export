#
# OdooMapper
#
# Gert Wijsman
# Dec 2024
#
import logging

from package.odoo.OdooInfo import OdooInfo
from package.odoo.OdooCustomer import OdooCustomer
from ..ImportLogging import setup_logging

logger = logging.getLogger(__name__)

class OdooMapper:

    def __init__(self, odoo_in_info, odoo_out_info):
        self.odoo_in_info = odoo_in_info
        self.odoo_out_info = odoo_out_info
        self.cache = {
            'customer': {} 
        }
        
    def get_customerid_for(self, cid):
        # get the customer from the in odoo
        # calculate the name of the customer
        # find the customer in the out odoo
        # (used to retrieve the parent, and cache the ids
        #  advisable to populate the cache on insert of customers)
        cache = self.cache['customer']
        if cid in cache.keys():
            return cache[cid] 
        oc = OdooCustomer(self.odoo_in_info, cid)
        ocn = oc.data()['name']
        domain = [[['name', '=', ocn]]]
        nc = self.odoo_out_info.kw_search_result('res.partner', domain)
        if len(nc) == 0:
            logger.error("No Result for %i (%s)", cid, ocn)
            return False
        else:
            nc = nc[0]
        domain = [nc]
        # print(self.odoo_out_info.kw_read_result('res.partner', domain))
        cache[cid] = nc
        return nc 
        
        
    def set_customerid_for(self, cid, nid):
        # fill the cache with mapping from cid to nid
        # (preferred to do on insert) 
        cache = self.cache['customer']
        cache[cid] = nid 

    def dump(self):
        print(self.cache)
