#
# OdooCountryFinder
#
# Gert Wijsman
# December 2024
#

import logging

from .OdooFinder import OdooFinder 
from .OdooCountry import OdooCountry

logger = logging.getLogger(__name__)

class OdooCountryFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'country'
        self.name = 'Country'

    def get_country_id_for_id(self, oid):
        oc = OdooCountry(self.odoo_in_info, oid)  
        name = oc.data()['name']
        nid = oc.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(oc)
        return nid
    
    def retrieve_new_id(self, country):
        country_name = country.data()['name']
        domain = [[['name', '=', country_name]]]
        new_countries = self.odoo_out_info.kw_search_result('res.country', domain)
        if len(new_countries) == 0:
            logger.warning("No country found for %s", country_name)
            return False 
        elif len(new_countries) > 1:
            logger.warning("More countries found for %s", country_name)
        nid = new_countries[0]
        country.data()['toid2025'] = nid
        country.set_cached_record()
        return nid 
