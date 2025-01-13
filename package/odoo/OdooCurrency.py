# 
# OdooCurrency
#
#
# Gert Wijsman
# January 2025
#

import logging
from .OdooObject import OdooObject 
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OdooCurrency(OdooObject, SqliteObject):

    def __init__(self, odoo_info, id, newvalue=None):
        if newvalue != None: 
            logger.debug("Init Currency: %i and new value: %s", id, newvalue)
            self.currency = {'name': newvalue, 'id': id, 'active': True, 'parent_id': False}
            self.id = id
            self.odoo_info = odoo_info
        else: 
            logger.debug("Init Currency: %i", id)
            super().__init__(odoo_info, id) 
            self.currency = self.get_from_odoo()
        self.set_cached_record() 

    def data(self):
        return self.currency

    def external_name(self):
        return "Currency" 

    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('res.currency', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def sqlite_table_name(self):
        return 'currency'

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

    def write_to_database(self, odoo_info):
        field_list = self.compile_field_list() 
        try:
            domain = [field_list] 
            result = odoo_info.kw_create('res.partner.currency', domain)
            self.data()['toid2025'] = result
            self.data()['migrated2025'] = True
            self.set_cached_record() 
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False
        return result 
