#
# migration engine
#
# Gert Wijsman
# Dec 2024
#

import logging

from package.odoo.OdooMapper import OdooMapper
from package.odoo.OdooCustomers import OdooCustomers
from package.odoo.OdooContacts import OdooContacts 
from package.odoo.OdooCustomer import OdooCustomer
from package.migration.MigrationCustomerFilter import MigrationCustomerFilter
from package.sqlite.SqliteDB import SqliteDB

logger = logging.getLogger(__name__)

class Migration:

    def __init__(self, odoo_in_info, odoo_out_info):
        self.odoo_in_info = odoo_in_info
        self.odoo_out_info = odoo_out_info

    def initialize(self):
        self.sdb = SqliteDB("/home/gert.wijsman/testgert.db")
        self.sdb.initialize_db()
        self.odoo_in_info.cache_db = self.sdb 

        self.customerfilter = MigrationCustomerFilter()
        self.customerfilter.start(self.odoo_in_info, self.sdb) 

        self.mapper = OdooMapper(self.odoo_in_info, self.odoo_out_info)


    def migrate_customers(self):
        domain = [
            [
                ['is_company', '=', True],
                ['customer', '=', True], 
                ['supplier', '=', False],
                ['active', '=', True],
                # ['name', 'like', 'American']
                # ['id', '=', 6788]
                # ['id', '=', 363] 
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
                ['supplier', '=', False],
                ['active', '=', True],
                # ['parent_id', '=', 762],
                # ['parent_id', '=', 363],
            ]
        ]
        # 470 En
        # 6923 AEP
        # 761 En (skip; Almelo)
        # 762 En (change Assen) 
        # 6788 Gert test
        # 363 hak 
        odoo_contacts = OdooContacts(self.odoo_in_info, domain) 
        for contact in odoo_contacts:
            logger.debug(contact)
            if contact.already_migrated():
                logger.warning("Already migrated contact for %i", contact.id)
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
                    logger.error("No action defined for %s",  contact)
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
                print(new_pid)
                contact.data()['parent_id'] = new_pid
                
            contact.write_to_database(self.odoo_out_info)
        
    def do(self):
        print("do")
        self.initialize()
        self.migrate_customers()
        self.migrate_contacts() 

