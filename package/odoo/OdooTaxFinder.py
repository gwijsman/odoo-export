#
# OdooTaxFinder
#
# Gert Wijsman
# January 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooTax import OdooTax

logger = logging.getLogger(__name__)

class OdooTaxFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'tax'
        self.name = 'Tax'

    def get_tax_id_for_id(self, oid):
        ot = OdooTax(self.odoo_in_info, oid)  
        name = ot.data()['name']
        nid = ot.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(ot)
        return nid
    
    def retrieve_new_id(self, tax):
        tax_name = tax.data()['name']
        domain = [[['name', '=', tax_name]]]
        new_taxs = self.odoo_out_info.kw_search_result('account.tax', domain)
        if len(new_taxs) == 0:
            logger.warning("No tax found for %s", tax_name)
            return False 
        elif len(new_taxs) > 1:
            logger.warning("More taxes found for %s", tax_name)
        nid = new_taxs[0]
        tax.data()['toid2025'] = nid
        tax.set_cached_record()
        return nid 
