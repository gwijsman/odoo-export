# 
# OdooCountry
#
#
# Gert Wijsman
# December 2025
#

import logging
from .OdooObject import OdooObject 
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)

class OdooCountry(OdooObject, SqliteObject):

    def __init__(self, odoo_info, id):
        logger.debug("Init Country: %i", id)
        super().__init__(odoo_info, id) 
        self.country = self.get_from_odoo()
        self.set_cached_record() 

    def data(self):
        return self.country

    def external_name(self):
        return "Country" 

    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('res.country', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def sqlite_table_name(self):
        return 'country'

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
