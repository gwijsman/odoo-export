#
# OdooCustomers
#
# wrapper with functionality specific for the customers list
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
from .OdooPartners import OdooPartners
from .OdooCustomer import OdooCustomer

logger = logging.getLogger(__name__)

class OdooCustomers(OdooPartners):

    def __init__(self, odoo_info, domain=[[]]):
        super().__init__(odoo_info, domain)
        logger.debug(self.__str__())

    def __str__(self):
        return f"OdooCustomers: List of {len(self.customers())} customers"

    def customers(self):
        return self.partners() 

    def customerids(self):
        return self.partnerids() 
        
    def get_list_details(self):
        for id in self.customerids():
            self.customers().append(OdooCustomer(self.odoo_info, id))
