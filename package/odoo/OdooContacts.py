#
# OdooContacts
#
# wrapper with functionality specific for the contacts list
# implemented an iter over the list
#
# domain could be: [[['is_company', '=', False]]]
#
# Gert Wijsman
# November 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging 
from .OdooPartners import OdooPartners
from .OdooContact import OdooContact

logger = logging.getLogger(__name__)

class OdooContacts(OdooPartners):

    def __init__(self, odoo_info, domain=[[]]):
        super().__init__(odoo_info, domain)
        logger.debug(self.__str__())

    def __str__(self):
        return f"OdooContacts: List of {len(self.contacts())} contacts"

    def contacts(self):
        return self.partners() 

    def contactids(self):
        return self.partnerids() 
        
    def get_list_details(self):
        for id in self.contactids():
            self.contacts().append(OdooContact(self.odoo_info, id))
