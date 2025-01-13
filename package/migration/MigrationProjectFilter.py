#
# MigrationProjectFilter
#
# filter and modifier for Projects
#
# Gert Wijsman
# December 2024

import logging
import csv
import time 
from time import gmtime, strftime

from package.migration.MigrationFilter import MigrationFilter
from package.ImportLogging import setup_logging

logger = logging.getLogger(__name__)

class MigrationProjectFilter(MigrationFilter):

    def __init__(self):
        super().__init__()
        self.csv_file = "project-filter.csv"
        self.migfilter = {}
        self.name = {}
        
    def start(self, odoo_info):
        self.odoo_info = odoo_info
        self.sdb = odoo_info.cache_db 
        self.read_csv()

    def filter(self, project):
        # return action needed and what action (what is a vector)
        # so False, None means no action needed (by the filter) mostly: just migrate
        # so True, 'delete' means do not migrate
        # so True, 'change' means to change the children to an other parent 
        # so True, 'none' means just migrate 
        # add migration reason 
        action, what = self.filter_by_id(project.id)
        if action:
            self.set_migration_reason(project, "mapaction"+what[0]) 
            return True, what 
        if self.has_relevant_tag(project):
            return True, ['none']
        if self.has_invoices(project):
            return True, ['none']
        if self.has_tasks_or_issues(project):
            return True, ['none']
        if self.has_recent_changes(project):
            return True, ['none']
        # no reason found to migrate, skip! 
        self.set_migration_reason(project, 'novalidreason')
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
            what = [action, self.name[contact_id]]
            return True, what 

    def read_csv(self):
        filename = self.csv_filename()
        with open(filename, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
                key = int(row[0])
                value = row[1].strip()
                self.migfilter[key] = value
                value2 = row[2].strip()
                self.name[key] = value2 
                logger.debug("Added migration filter item for %i (%s) with action %s", key, value2, value)
        
    def new_value_for(self, key):
        return self.migfilter[key] 

    def has_relevant_tag(self, project):
        relevant_tags = [48,49,64,18,65,44,45,46,17,55,9,25,53]
        logger.debug("Relevant? : %s", project)
        for tag_id in project.data()['category_id']:
            if tag_id in relevant_tags:
                self.set_migration_reason(project, 'tag %i'%tag_id) 
                return True
        return False 

    def has_invoices(self, project):
        invoices = project.data()['invoice_ids']
        if len(invoices) > 0:
            self.set_migration_reason(project, 'invoice') 
            return True
        return False 

    def has_tasks_or_issues(self, project):
        tasks = project.data()['task_count']
        if tasks > 0:
            self.set_migration_reason(project, 'has tasks') 
            return True
        issues = project.data()['issue_count']
        if issues > 0:
            self.set_migration_reason(project, 'has issues') 
            return True
        sales_orders = project.data()['sale_order_count']
        if sales_orders > 0:
            self.set_migration_reason(project, 'has sales orders') 
            return True
        purchase_orders = project.data()['purchase_order_count']
        if purchase_orders > 0:
            self.set_migration_reason(project, 'has purchase orders') 
            return True
        
        return False 

    def has_recent_changes(self, project):
        logger.warning("TODO recent changes for project %s", project)
        cd = project.data()['create_date']
        if self.date_relevant(cd):
            self.set_migration_reason(project, "creationdate")
            return True 
        lud = project.data()['__last_update']
        if self.date_relevant(lud):
            self.set_migration_reason(project, "lastupdate")
            return True 
        wd = project.data()['write_date']
        if self.date_relevant(wd):
            self.set_migration_reason(project, "writedate")
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
    
    def set_migration_reason(self, project, reason):
        project.data()['reasonmigration2025'] = reason 
        
    
#    supplier_invoice_count
#    purchase_order_count
