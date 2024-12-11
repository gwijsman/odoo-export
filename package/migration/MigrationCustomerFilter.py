#
# MigrationCustomerFilter
#
# filter and modifier for Cusomers
#
# Gert Wijsman
# November 2024

import logging
import csv

from .MigrationFilter import MigrationFilter 
from ..ImportLogging import setup_logging

logger = logging.getLogger(__name__)

class MigrationCustomerFilter(MigrationFilter):

    def __init__(self):
        super().__init__()
        self.csv_file = "customer-filter.csv"
        self.migfilter = {}
        self.map_id = {}
        self.new_id = {}

    def start(self):
        self.read_csv()

    def filter(self, customer):
        return self.filter_by_id(customer.id)

    def filter_by_id(self, customer_id):
        action = None 
        if customer_id in self.migfilter:
            action = self.migfilter[customer_id]
        if action is None:
            logger.debug("No Action needed for: %s", customer_id)
            return False, None 
        else:
            logger.debug("Action needed for: %s", customer_id)
            logger.debug("Action: %s", action)
            return True, action 

    def read_csv(self):
        filename = self.csv_filename()
        with open(filename, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                key = int(row[0])
                value = row[1].strip()
                logger.debug("Added migration filter item for %i with action %s", key, value)
                self.migfilter[key] = value
                value2 = row[2].strip()
                self.map_id[key] = value2 
        
    def new_value_for(self, key):
        return self.migfilter[key] 

    def new_id_for(self, key):
        return self.map_id[key] 

    def set_new_odoo_id_for(self, key, nid):
        self.new_id[key] = nid

    def get_new_odoo_id_for(self, key):
        if key in self.new_id.keys():
            nid = self.new_id[key]
        else:
            nid = None 
        return nid 
        
