#
# migration engine
#
# Gert Wijsman
# Dec 2024
#

import logging
import os

from package.odoo.OdooCustomers import OdooCustomers
from package.odoo.OdooContacts import OdooContacts 
from package.odoo.OdooCustomer import OdooCustomer
from package.odoo.OdooProjects import OdooProjects
from package.odoo.OdooFinders import OdooFinders 
from package.migration.MigrationCustomerFilter import MigrationCustomerFilter
from package.migration.MigrationContactFilter import MigrationContactFilter
from package.sqlite.SqliteDB import SqliteDB

logger = logging.getLogger(__name__)

class Migration:

    def __init__(self, odoo_in_info, odoo_out_info):
        self.odoo_in_info = odoo_in_info
        self.odoo_out_info = odoo_out_info

    def initialize(self):
        sqlitedbfile = os.getenv('SQLITEFILE')
        self.sdb = SqliteDB(sqlitedbfile)
        self.sdb.initialize_db()
        self.odoo_in_info.cache_db = self.sdb 

        self.contactfilter = MigrationContactFilter()
        self.contactfilter.start(self.odoo_in_info) 

        self.customerfilter = MigrationCustomerFilter()
        self.customerfilter.start(self.odoo_in_info) 
        self.customerfilter.set_contact_filter(self.contactfilter)

        OdooFinders.initialize(self.odoo_in_info, self.odoo_out_info)  

    def check_config_target_db(self):
        language_codes = [ 'en_US', 'nl_NL', 'de_DE']
        for lang in language_codes:
            domain = [[['code', '=', lang]]]
            lid = self.odoo_out_info.kw_search_result('res.lang', domain)
            if len(lid) == 0:
                logger.error('Language configuration wrong for %s, please correct', lang)
                exit(1)
            lr = self.odoo_out_info.kw_read_result('res.lang', lid)
            name = lr[0]['name']
            active = lr[0]['active']
            if active is False:
                logger.error('Language configuration wrong for %s (%s), please correct (active = %s)', lang, name, str(active))

    def migrate_customers(self):
        domain = [
            [
                ['is_company', '=', True],
                ['customer', '=', True], 
                # ['supplier', '=', False], ==> not valid because for example Vitens is supplier too?!?
                ['active', '=', True],
                # ['name', 'like', 'American']
                ['id', '=', 693]
                # ['id', '=', 363] 
                # ['id', '=', 438] 
                # ['name', 'like', 'Enexis']
            ]
        ]
        odoo_customers = OdooCustomers(self.odoo_in_info, domain)
        for customer in odoo_customers:
            logger.debug(customer)
            if customer.already_migrated():
                logger.warning("Already migrated customer for %i", customer.id)
                continue 
            action, what = self.customerfilter.filter(customer)
            if action:
                if what[0] in ['delete']:
                    logger.info("Skip this customer: %i : %s", customer.id, customer)
                    customer.set_cached_record() 
                    continue 
                if what[0] in ['change']:
                    logger.info("Skip this customer: %i : %s", customer.id, customer)
                    customer.data()['mappedinid2025'] = what[1]
                    customer.data()['migrated2025'] = True 
                    customer.set_cached_record() 
                    continue 
            #customer.debug_dump()
            #customer.debug_dump_keys()
            nid = customer.write_to_database(self.odoo_out_info)

    def migrate_contacts(self):
        domain = [
            [
                ['is_company', '=', False],
                ['customer', '=', True], 
                #['supplier', '=', False],
                ['active', '=', True],
                ['parent_id', '=', 693],
                # ['parent_id', '=', 363],
                # ['id', '=', 8112]
            ]
        ]
        # 470 En
        # 6923 AEP
        # 761 En (skip; Almelo)
        # 762 En (change Assen) 
        # 6788 Gert test
        # 363 hak 
        # 438 cox 
        # 693 Vitens
        odoo_contacts = OdooContacts(self.odoo_in_info, domain) 
        for contact in odoo_contacts:
            logger.debug(contact)
            if contact.already_migrated():
                logger.warning("Already migrated contact for %i", contact.id)
                continue 

            action, what = self.contactfilter.filter(contact)
            if action:
                if what[0] in ['delete']:
                    logger.info("Skip this contact: %i : %s", contact.id, contact)
                    contact.set_cached_record() 
                    continue 

            mcustomer = None
            pcustomer = None
            if contact.data()['parent_id'] != False: 
                pid = contact.data()['parent_id'][0]
                pcustomer = OdooCustomer(self.odoo_in_info, pid)
                action, what = self.customerfilter.filter(pcustomer)
                if action:
                    if what[0] in ['delete']:
                        logger.info("Skip this contact: %i : %s", contact.id, contact)
                        contact.data()['reasonmigration2025'] = 'delete'
                        contact.set_cached_record()
                        pcustomer.set_cached_record()
                        continue 
                    elif what[0] in ['change']:
                        # change the parent id
                        mid = int(what[1]) 
                        mcustomer = OdooCustomer(self.odoo_in_info, mid)
                    elif what in ['none']:
                        pass 
                    else:
                        logger.error("Wrong action, %s", what) 
                else:
                    logger.debug("No action defined for %s",  contact)
            else:
                contact.data()['nocustomer2025'] = True

            if mcustomer is None:
                npcustomer = pcustomer
            else:
                npcustomer = mcustomer
            if npcustomer == None:
                #contact.data()['parent_id'] = False 
                pass 
            else: 
                new_pid = npcustomer.migrated_to()
                contact.data()['parent_id'] = new_pid
                
            contact.write_to_database(self.odoo_out_info)
        
    def migrate_projects(self):
        domain = [
            [
                ['state', '=', 'open'],
                #['analytic_account_id', ]
                #['customer', '=', True], 
                # ['supplier', '=', False], ==> not valid because for example Vitens is supplier too?!?
                #['active', '=', True],
                # ['name', 'like', 'American']
                #['id', '=', 693]
                # ['id', '=', 363] 
                # ['id', '=', 438] 
                # ['name', 'like', 'Enexis']
            ]
        ]
        odoo_projects = OdooProjects(self.odoo_in_info, domain)
        outputfolder = os.getenv('TEXT_OUTPUT_FOLDER')
        filename = outputfolder + '/projects.csv'
        try:
            f = open(filename, 'w') # replace with 'x' later (when no overwriting needed!) 
        except Exception:
            logger.error("Failed opening file: %s", filename)
            exit(1) 
        for project in odoo_projects:
            logger.debug(project)
            if project.already_migrated():
                logger.warning("Already migrated project for %i", project.id)
                # continue 
            #action, what = self.projectfilter.filter(project)
            #if action:
            #    if what[0] in ['delete']:
            #        logger.info("Skip this project: %i : %s", project.id, project)
            #        project.set_cached_record() 
            #        continue 
            #    if what[0] in ['change']:
            #        logger.info("Skip this project: %i : %s", project.id, project)
            #        project.data()['mappedinid2025'] = what[1]
            #        project.data()['migrated2025'] = True 
            #        project.set_cached_record() 
            #        continue 
            #project.debug_dump()
            #project.debug_dump_keys()
            # nid = project.write_to_database(self.odoo_out_info)
            #project.report() 
            project.write_info_to_csv(f)
        f.close() 

    def do(self):
        self.check_config_target_db()
        self.initialize()
        #self.migrate_customers()
        #self.migrate_contacts() 
        self.migrate_projects()

