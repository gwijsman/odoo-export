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
from .OdooCustomer import OdooCustomer

logger = logging.getLogger(__name__)

class OdooCustomers:
    def __init__(self, odoo_info, domain=[[]]):
        self.odoo_info = odoo_info
        self.domain = domain 
        self.list_of_customerids = []
        self.list_of_customers = []
        self.get_list()
        logger.debug(self.__str__())

    def __str__(self):
        return f"OdooCustomers: List of {len(self.list_of_customers)} customers"

    def __iter__(self):
        self.index = 0
        return self 

    def __next__(self):
        if self.index < len(self.list_of_customers):
            x = self.index 
            self.index += 1
            item = self.list_of_customers[x] 
            return item 
        else: 
            raise StopIteration
    
    def get_list(self):
        self.list_of_customerids = self.odoo_info.kw_search_result('res.partner', self.domain)
        for id in self.list_of_customerids:
            self.list_of_customers.append(OdooCustomer(self.odoo_info, id))

    def customers(self):
        return self.list_of_customers 

    def first(self):
        if len(self.list_of_customers) == 0:
            return False
        else:
            return self.list_of_customers[0]
