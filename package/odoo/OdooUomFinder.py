#
# OdooUomFinder (unit of measure)
#
# Gert Wijsman
# January 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooUom import OdooUom

logger = logging.getLogger(__name__)

class OdooUomFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'uom'
        self.name = 'uom'

    def get_uom_id_for_id(self, oid):
        ou = OdooUom(self.odoo_in_info, oid)  
        name = ou.data()['name']
        nid = ou.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(ou)
        return nid
    
    def retrieve_new_id(self, uom):
        uom_name = uom.data()['name']
        self.correct_name(uom)
        domain = [[['name', '=', uom_name]]]
        new_uoms = self.odoo_out_info.kw_search_result('uom.uom', domain)
        if len(new_uoms) == 0:
            logger.warning("No uom found for %s", uom_name)
            return False 
        elif len(new_uoms) > 1:
            logger.warning("More uoms found for %s", uom_name)
        nid = new_uoms[0]
        uom.data()['toid2025'] = nid
        uom.set_cached_record()
        return nid 

    def correct_name(self, uom):
        uom_name = uom.data()['name']
        if uom_name == 'Unit(s)':
            uom.data()['name'] = 'Units'
