#
# MigrationContactFilter
#
# filter and modifier for Contacts
#
# Gert Wijsman
# December 2024

import logging
import csv
import time 
from time import gmtime, strftime

from package.migration.MigrationFilter import MigrationFilter
from package.odoo.OdooContacts import OdooContacts 
from package.ImportLogging import setup_logging

logger = logging.getLogger(__name__)

class MigrationContactFilter(MigrationFilter):

    def __init__(self):
        super().__init__()
        self.csv_file = "contact-filter.csv"
        self.migfilter = {}
        self.map_id = {}
        
    def start(self, odoo_info):
        self.odoo_info = odoo_info
        self.sdb = odoo_info.cache_db 
        self.read_csv()

    def filter(self, contact):
        # return action needed and what action (what is a vector)
        # so False, None means no action needed (by the filter) mostly: just migrate
        # so True, 'delete' means do not migrate
        # so True, 'change' means to change the children to an other parent 
        # so True, 'none' means just migrate 
        # add migration reason 
        action, what = self.filter_by_id(contact.id)
        if action:
            self.set_migration_reason(contact, "mapaction"+what[0]) 
            return True, what 
        if self.has_relevant_tag(contact):
            return True, ['none']
        if self.has_invoices(contact):
            return True, ['none']
        if self.has_tasks_or_issues(contact):
            return True, ['none']
        if self.has_recent_changes(contact):
            return True, ['none']
        # no reason found to migrate, skip! 
        self.set_migration_reason(contact, 'novalidreason')
        return True, ['delete']

    def filter_by_id(self, contact_id):
        # in an action is needed return true and the action needed
        action = None
        what = []
        if contact_id in self.migfilter:
            action = self.migfilter[contact_id]
        if action is None:
            logger.debug("No Action needed for: %s", contact_id)
            return False, None 
        else:
            logger.debug("Action needed for: %s", contact_id)
            logger.debug("Action: %s", action)
            what = [action, self.map_id[contact_id]]
            return True, what 

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

    def has_relevant_tag(self, contact):
        relevant_tags = [48,49,64,18,65,44,45,46,17,55,9,25,53]
        logger.debug("Relevant? : %s", contact)
        for tag_id in contact.data()['category_id']:
            if tag_id in relevant_tags:
                self.set_migration_reason(contact, 'tag %i'%tag_id) 
                return True
        return False 

    def has_invoices(self, contact):
        invoices = contact.data()['invoice_ids']
        if len(invoices) > 0:
            self.set_migration_reason(contact, 'invoice') 
            return True
        return False 

    def has_tasks_or_issues(self, contact):
        tasks = contact.data()['task_count']
        if tasks > 0:
            self.set_migration_reason(contact, 'has tasks') 
            return True
        issues = contact.data()['issue_count']
        if issues > 0:
            self.set_migration_reason(contact, 'has issues') 
            return True
        sales_orders = contact.data()['sale_order_count']
        if sales_orders > 0:
            self.set_migration_reason(contact, 'has sales orders') 
            return True
        purchase_orders = contact.data()['purchase_order_count']
        if purchase_orders > 0:
            self.set_migration_reason(contact, 'has purchase orders') 
            return True
        
        return False 

    def has_recent_changes(self, contact):
        logger.warning("TODO recent changes for contact %s", contact)
        cd = contact.data()['create_date']
        if self.date_relevant(cd):
            self.set_migration_reason(contact, "creationdate")
            return True 
        lud = contact.data()['__last_update']
        if self.date_relevant(lud):
            self.set_migration_reason(contact, "lastupdate")
            return True 
        wd = contact.data()['write_date']
        if self.date_relevant(wd):
            self.set_migration_reason(contact, "writedate")
            return True 
        return False 

    def date_relevant(self, s):
        #
        # s string in ODOO time format: 2016-07-02 08:13:24
        #
        five_year = time.strptime("01/01/2019", "%d/%m/%Y")
        #print("five: ", strftime("%Y-%m-%d %H:%M:%S", five_year))
        cdate = time.strptime(s, "%Y-%m-%d %H:%M:%S")
        #print("current: ", strftime("%Y-%m-%d %H:%M:%S", cdate))
        #print("relevant? : ", (cdate > five_year))
        return cdate > five_year 
    
    def set_migration_reason(self, contact, reason):
        contact.data()['reasonmigration2025'] = reason 
        
    
#    supplier_invoice_count
#    purchase_order_count
