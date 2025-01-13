#
# OdooPartnerFinder
#
# Gert Wijsman
# Januari 2025
#

import logging

from .OdooFinder import OdooFinder 
from .OdooPartner import OdooPartner

logger = logging.getLogger(__name__)

class OdooPartnerFinder(OdooFinder):

    def __init__(self, odoo_in_info, odoo_out_info):
        super().__init__(odoo_in_info, odoo_out_info)
        self.key = 'partner'
        self.name = 'Partner'

    def set_related_finders(self, customer_finder, contact_finder):
        self.customer_finder = customer_finder
        self.contact_finder = contact_finder

    def get_partner_id_for_id(self, oid):
        ocuid = self.customer_finder.get_customer_id_for_id(oid)
        if ocuid is False:
            ocoid = self.contact_finder.get_contact_id_for_id(oid)
            nid = ocoid
        else:
            nid = ocuid
        return nid
    
