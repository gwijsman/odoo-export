#
# OdooSalesOrders
#
# wrapper with functionality for the sales order list
# implemented an iter over the list
#
#
# Gert Wijsman
# Januari 2025
#
# inspriation:
# I love Object Oriented programming 
#

import logging 
from .OdooSalesOrder import OdooSalesOrder

logger = logging.getLogger(__name__)

class OdooSalesOrders:

    def __init__(self, odoo_info, domain=[[]]):
        self.odoo_info = odoo_info
        self.domain = domain 
        self.list_of_sales_order_ids = []
        self.list_of_sales_orders = []
        self.get_list_ids()
        self.get_list_details()
        logger.debug(self.__str__())

    def __str__(self):
        return f"OdooSalesOrders: List of {len(self.sales_orders())} sales_orders"

    def sales_orders(self):
        return self.list_of_sales_orders 

    def sales_order_ids(self):
        return self.list_of_sales_order_ids 

    def __iter__(self):
        self.index = 0
        return self 

    def __next__(self):
        if self.index < len(self.sales_orders()):
            x = self.index 
            self.index += 1
            item = self.sales_orders()[x] 
            return item 
        else: 
            raise StopIteration
    
    def get_list_ids(self):
        self.list_of_sales_order_ids = self.odoo_info.kw_search_result('sale.order', self.domain)

    def get_list_details(self):
        for id in self.sales_order_ids():
            self.sales_orders().append(OdooSalesOrder(self.odoo_info, id))

    def first(self):
        if len(self.sales_orders()) == 0:
            return False
        else:
            return self.sales_orders()[0]

