#
# OdooStateFinder
#
# Gert Wijsman
# December 2024
#

import logging

from .OdooFinder import OdooFinder 
from .OdooState import OdooState

logger = logging.getLogger(__name__)

class OdooStateFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'state'
        self.name = 'State'

    def get_state_id_for_id(self, oid):
        os = OdooState(self.odoo_in_info, oid)  
        name = os.data()['name']
        nid = os.sqlite_to_id()
        if nid is False:
            nid = self.retrieve_new_id(os)
        return nid
    
    def retrieve_new_id(self, state):
        state_name = state.data()['name']
        domain = [[['name', '=', state_name]]]
        new_states = self.odoo_out_info.kw_search_result('res.country.state', domain)
        if len(new_states) == 0:
            logger.warning("No state found for %s", state_name)
            return False 
        elif len(new_states) > 1:
            logger.warning("More states found for %s", state_name)
        nid = new_states[0]
        state.data()['toid2025'] = nid
        state.set_cached_record()
        return nid 
