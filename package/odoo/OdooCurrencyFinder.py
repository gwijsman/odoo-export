#
# OdooCurrencyFinder
#
# Gert Wijsman
# January 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooCurrency import OdooCurrency

logger = logging.getLogger(__name__)

class OdooCurrencyFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'currency'
        self.name = 'Currency'
        self.setup_target_currencies()

    def get_currency_id_for_id(self, oid):
        oc = OdooCurrency(self.odoo_in_info, oid)  
        name = oc.data()['name']
        nid = oc.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(oc)
        return nid
    
    def retrieve_new_id(self, currency):
        currency_name = currency.data()['name']
        domain = [[['name', '=', currency_name]]]
        new_currencies = self.odoo_out_info.kw_search_result('res.currency', domain)
        if len(new_currencies) == 0:
            logger.warning("No currency found for %s", currency_name)
            return False 
        elif len(new_currencies) > 1:
            logger.warning("More currencies found for %s", currency_name)
        nid = new_currencies[0]
        currency.data()['toid2025'] = nid
        currency.set_cached_record()
        return nid 

    def setup_target_currencies(self):
        relevant = [1, 3, 5, 22, 150, 29]
        for cid in relevant:
            if self.get_currency_id_for_id(cid) is False:
                oc = OdooCurrency(self.odoo_in_info, cid)  
                name = oc.data()['name']
                #oc.write_to_database(self.odoo_out_info)

    def get_migration_currency(self):
        return self.get_currency_id_for_id(999)