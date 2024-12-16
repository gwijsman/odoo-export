#
# MigrationCustomerFilter
#
# filter and modifier for Cusomers
#
# Gert Wijsman
# November 2024

import logging
import csv
import time 

from package.migration.MigrationFilter import MigrationFilter
from package.odoo.OdooContacts import OdooContacts 
from package.ImportLogging import setup_logging

logger = logging.getLogger(__name__)

class MigrationCustomerFilter(MigrationFilter):

    def __init__(self):
        super().__init__()
        self.csv_file = "customer-filter.csv"
        self.migfilter = {}
        self.map_id = {}
        
    def start(self, odoo_info, sqlitedb):
        self.odoo_info = odoo_info
        self.sdb = sqlitedb 
        self.read_csv()

    def filter(self, customer):
        # return action needed and what action
        # so False, None means no action needed just migrate
        # so True, 'delete' means do not migrate
        # so True, 'change' means to change the children to an other parent (id in customer.data()['migrateto2025'])  
        # does this customer (or its contacts) has some tag we selected?
        # add migration reason to customer.data()['reasonmigrateto2025'])

        action, what = self.filter_by_id(customer.id)
        if action:
            self.set_migration_reason(customer, "mapaction"+what[0]) 
            return True, what 
        
        if self.has_relevant_tag(customer):
            return False, None
        # does this customer has some connected objects in ODOO?
        # which:
        # * invoices
        if self.has_invoices(customer):
            return False, None
            
        # * tasks and issues (shorter than 5 years)
        if self.has_tasks_or_issues(customer):
            return False, None
        
        # * contacts changed within 5 years
        # does this customer had some related action after some date
        if self.has_recent_changes(customer):
            return False, None

        # mark the record as skipped when not migrated (not in the filter...)
        self.set_migration_reason(customer, "delete")
        return True, ['delete']

    def filter_by_id(self, customer_id):
        # in an action is needed return true and the action needed
        action = None
        what = []
        if customer_id in self.migfilter:
            action = self.migfilter[customer_id]
        if action is None:
            logger.debug("No Action needed for: %s", customer_id)
            return False, None 
        else:
            logger.debug("Action needed for: %s", customer_id)
            logger.debug("Action: %s", action)
            what = [action, self.map_id[customer_id]]
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

    def has_relevant_tag(self, customer):
        relevant_tags = [48,49,64,18,65,44,45,46,17,55,9,25,53]
        cuid = customer.id 
        domain = [
            [
                ['is_company', '=', False],
                ['supplier', '=', False],
                ['active', '=', True],
                ['parent_id', '=', cuid],
            ]
        ]
        odoo_contacts = OdooContacts(self.odoo_info, domain) 
        for contact in odoo_contacts:
            logger.debug("Relevant? : %s", contact)
            for tag_id in contact.data()['category_id']:
                if tag_id in relevant_tags:
                    has_tag = True
                    self.set_migration_reason(customer, 'tag %i'%tag_id) 
                    return True
        return False 

    def has_invoices(self, customer):
        invoices = customer.data()['invoice_ids']
        if len(invoices) > 0:
            self.set_migration_reason(customer, 'invoice') 
            return True
        return False 

    def has_tasks_or_issues(self, customer):
        tasks = customer.data()['task_count']
        if tasks > 0:
            self.set_migration_reason(customer, 'has tasks') 
            return True
        issues = customer.data()['issue_count']
        if issues > 0:
            self.set_migration_reason(customer, 'has issues') 
            return True
        sales_orders = customer.data()['sale_order_count']
        if sales_orders > 0:
            self.set_migration_reason(customer, 'has sales orders') 
            return True
        purchase_orders = customer.data()['purchase_order_count']
        if sales_orders > 0:
            self.set_migration_reason(customer, 'has purchase orders') 
            return True
        return False 

    def has_recent_changes(self, customer):
        logger.warning("TODO recent changes for customer %s", customer)
        cd = customer.data()['create_date']
        if self.date_relevant(cd):
            self.set_migration_reason(customer, "creationdate")
            return True 
        lud = customer.data()['__last_update']
        if self.date_relevant(lud):
            self.set_migration_reason(customer, "lastupdate")
            return True 
        wd = customer.data()['write_date']
        if self.date_relevant(wd):
            self.set_migration_reason(customer, "writedate")
            return True 
        return False 

    def date_relevant(self, s):
        #
        # s string in ODOO time format: 2016-07-02 08:13:24
        #
        five_year = time.strptime("01/01/2019", "%d/%m/%Y")
        date = time.strptime(s, "%Y-%m-%d %H:%M:%S")
        return date > five_year 
              
        
    
    def set_migration_reason(self, customer, reason):
        customer.data()['reasonmigration2025'] = reason 
        
    
#    supplier_invoice_count
#    purchase_order_count
