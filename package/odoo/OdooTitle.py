# 
# OdooTitle
#
#
# Gert Wijsman
# January 2025
#

import logging
from .OdooObject import OdooObject 
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)

class OdooTitle(OdooObject, SqliteObject):

    def __init__(self, odoo_info, id):
        logger.debug("Init Title: %i", id)
        super().__init__(odoo_info, id) 
        self.title = self.get_from_odoo()
        self.set_cached_record() 

    def data(self):
        return self.title

    def external_name(self):
        return "Title" 

    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('res.partner.title', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def sqlite_table_name(self):
        return 'title'

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
            result = odoo_info.kw_create('res.partner.title', domain)
            self.data()['toid2025'] = result
            self.data()['migrated2025'] = True
            self.set_cached_record() 
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False
        return result 
