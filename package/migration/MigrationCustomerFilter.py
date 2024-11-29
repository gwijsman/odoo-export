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

    def start(self):
        self.read_csv()

    def filter(self, customer):
        action = None 
        if customer.id in self.migfilter:
            action = self.migfilter[customer.id]
        if action is None:
            logger.debug("No Action needed for: %s", customer)
            return False, None 
        else:
            logger.debug("Action needed for: %s", customer)
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
        
