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
from package.migration.MigrationCustomerFilter import MigrationCustomerFilter

logger = logging.getLogger(__name__)

class Migration:

    def __init__(self, odoo_in_info, odoo_out_info):
        self.odoo_in_info = odoo_in_info
        self.odoo_out_info = odoo_out_info

    def initialize(self):
        self.customerfilter = MigrationCustomerFilter()
        self.customerfilter.start() 

        self.mapper = OdooMapper(self.odoo_in_info, self.odoo_out_info) 


    def migrate_customers(self):
        domain = [
            [
                ['is_company', '=', True],
                ['supplier', '=', False],
                ['active', '=', True],
                # ['name', 'like', 'American']
            ]
        ]
        odoo_customers = OdooCustomers(self.odoo_in_info, domain) 
        for customer in odoo_customers:
            logger.debug(customer)
            action, what = self.customerfilter.filter(customer)
            if action:
                if what in ['delete', 'change']:
                    logger.info("Skip this customer: %i : %s", customer.id, customer)
                    continue 
            # customer.debug_dump()
            # customer.debug_dump_keys()
            nid = customer.write_to_database(self.odoo_out_info)
            self.mapper.set_customerid_for(customer.id, nid)

            self.mapper.dump()

    def migrate_contacts(self):
        domain = [
            [
                ['is_company', '=', False],
                ['supplier', '=', False],
                ['active', '=', True],
#                ['parent_id', '=', 6923],
            ]
        ]
        # 470 En
        # 6923 AEP
        # 761 En 
        # 762 En 
        odoo_contacts = OdooContacts(self.odoo_in_info, domain) 
        for contact in odoo_contacts:
            logger.debug(contact)
            #        action, what = self.customerfilter.filter(customer)
            #        if action:
            #            if what in ['delete', 'change']:
            #                logger.info("Skip this customer: %i : %s", customer.id, customer)
            #                continue 
            # customer.debug_dump()
            # customer.debug_dump_keys()
            if contact.data()['parent_id'] != False: 
                pid = contact.data()['parent_id'][0]
                action, what = self.customerfilter.filter_by_id(pid)
                if action:
                    if what in ['delete']:
                        logger.info("Skip this contact: %i : %s", contact.id, contact)
                        continue 
                    elif what in ['change']:
                        # change the parent id
                        npid = int(self.customerfilter.new_id_for(pid))
                        new_pid = self.mapper.get_customerid_for(npid)
                        contact.data()['parent_id'] = new_pid
                    elif what in ['none']:
                        new_pid = self.mapper.get_customerid_for(pid)
                        contact.data()['parent_id'] = new_pid
                    else:
                        logger.error("Wrong action, %s", what) 
                else:
                    logger.error("No action defined for %s",  contact)
                    new_pid = self.mapper.get_customerid_for(pid)
                    contact.data()['parent_id'] = new_pid
            contact.write_to_database(self.odoo_out_info) 
        
    def do(self):
        print("do")
        self.initialize()
        self.migrate_customers()
        self.migrate_contacts() 

