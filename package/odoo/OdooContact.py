#
# OdooContact
#
# wrapper with functionality specific for the contact itself
#
# 
# Gert Wijsman
# November 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging
from .OdooPartner import OdooPartner
from .OdooCustomer import OdooCustomer 
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)

class OdooContact(OdooPartner, SqliteObject):
    def __init__(self, odoo_info, id):
        logger.debug("Init Contact: %i", id)
        super().__init__(odoo_info, id)

    def external_name(self):
        return "Contact" 
        
    def write_to_database_keys(self):
        return [
            'name',
            'email',  
            'active',
            'is_company',
            'street',
            'street2',
            'zip',
            'city', 
            'website',
            'function',
            'title',
            'mobile',
            'phone',
#            'company_id',
            'parent_id',
            'country_id',
            'state_id', 
            'lang',
            'category_id',
            'comment',
        ]

    def get_company(self, parent_id):
        return OdooCustomer(self.odoo_info, parent_id) 

    # def get_join_info(self, odoo_out_info):
    #     print("FIXME") 
    #     #self.company = self.get_company(self.data()['parent_id'][0])
    #     #name = self.company.data()['name'] 
    #     #target_id = OdooCustomer.get_target_id(odoo_out_info, 'name', name)
    #     if not self.data()['parent_id']: 
    #         pid = self.data()['parent_id'][0]
    #         p = OdooCustomer()

    #     target_id = 0 
    #     self.data()['parent_id'] = target_id 

    def sqlite_table_name(self):
        return 'contact'

    def sqlite_id(self):
        return self.id

    def sqlite_name(self):
        return self.data()['name'] 

    def sqlite_migrated(self):
        if 'migrated2025' in self.data().keys():
            return self.data()['migrated2025']
        else:
            return False 

    def sqlite_reason(self):
        if 'reasonmigration2025' in self.data().keys():
            return self.data()['reasonmigration2025']
        else:
            return False 

    def sqlite_to_id(self):
        if 'toid2025' in self.data().keys():
            return self.data()['toid2025']
        else:
            return False 
