#
# OdooPartners
#
# wrapper with functionality for the partner list
# implemented an iter over the list
#
# domain could be: [[['is_company', '=', True]]]
#
# Gert Wijsman
# November 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging 
from .OdooPartner import OdooPartner 

logger = logging.getLogger(__name__)

class OdooPartners:

    def __init__(self, odoo_info, domain=[[]]):
        self.odoo_info = odoo_info
        self.domain = domain 
        self.list_of_partnerids = []
        self.list_of_partners = []
        self.get_list_ids()
        self.get_list_details()
        logger.debug(self.__str__())

    def __str__(self):
        return f"OdooPartners: List of {len(self.partners())} partners"

    def partners(self):
        return self.list_of_partners 

    def partnerids(self):
        return self.list_of_partnerids 

    def __iter__(self):
        self.index = 0
        return self 

    def __next__(self):
        if self.index < len(self.partners()):
            x = self.index 
            self.index += 1
            item = self.partners()[x] 
            return item 
        else: 
            raise StopIteration
    
    def get_list_ids(self):
        self.list_of_partnerids = self.odoo_info.kw_search_result('res.partner', self.domain)

    def get_list_details(self):
        for id in self.partnerids():
            self.partners().append(OdooPartner(self.odoo_info, id))

    def first(self):
        if len(self.partners()) == 0:
            return False
        else:
            return self.partners()[0]
