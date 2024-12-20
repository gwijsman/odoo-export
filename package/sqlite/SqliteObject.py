#
# SqliteObject
#
#
# Gert Wijsman
# Dec 2024
#

import json 
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR) 

class SqliteObject:

    def store_in_sqlite(self, db):
        # Store myself in sqlite
        # add all known data in json format
        # remove the old record first 
        self.remove_old_first(db)
        jo = json.dumps(self.data())
        sql = "INSERT INTO %s(id, name, migrated, reason, to_id, json) VALUES (?, ?, ?, ?, ?, ?)"%(self.sqlite_table_name())
        dbdata = (self.sqlite_id(),
                  self.sqlite_name(),
                  self.sqlite_migrated(),
                  self.sqlite_reason(),
                  self.sqlite_to_id(), 
                  jo)
        db.exec_sql(sql, dbdata)
        logger.debug("stored json data in sqlite: %i", len(jo))
        
    # we need the method data() on the child class
    # we need the method sqlite_table_name() on the child class
    # override sqlite_id and sqlite_name on will 
    
    def sqlite_table_name(self):
        return 'notablenameyet'

    def sqlite_id(self):
        return self.id

    def sqlite_name(self):
        return self.display_name

    def remove_old_first(self, db):
        id = self.sqlite_id()
        table = self.sqlite_table_name()
        sql = "SELECT id, name FROM %s WHERE id=%i"%(table, id)
        logger.debug("SQL Statement is: %s",sql)
        result = db.exec_sql(sql)
        rec = result.fetchone()
        if rec == None:
            # Nothing to remove 
            return
        sql = "DELETE FROM %s WHERE id=%i"%(table, id)
        logger.debug("SQL Statement is: %s",sql)
        result = db.exec_sql(sql)

    def already_migrated(self):
        cdb = self.odoo_info.cache_db
        id = self.sqlite_id()
        table = self.sqlite_table_name()
        sql = "SELECT id, name, migrated, reason, to_id FROM %s WHERE id=%i"%(table, id)
        logger.debug("SQL Statement is: %s",sql)
        result = cdb.exec_sql(sql)
        rec = result.fetchone()
        if rec == None:
            return False
        return rec[2] 

    def migrated_to(self):
        cdb = self.odoo_info.cache_db
        id = self.sqlite_id()
        table = self.sqlite_table_name()
        sql = "SELECT id, name, migrated, reason, to_id FROM %s WHERE id=%i"%(table, id)
        logger.debug("SQL Statement is: %s",sql)
        result = cdb.exec_sql(sql)
        rec = result.fetchone()
        if rec == None:
            return False
        return rec[4] 
    
    def get_cached_record(self):
        #
        # return False if not cached
        # rerurns a dictionary with the values otherwise retrieved from ODOO
        #
        cdb = self.odoo_info.cache_db
        if cdb == False: 
            return False 
        try:
            sql = "SELECT * FROM %s WHERE id = %i"%(self.sqlite_table_name(), self.id)
            result = cdb.exec_sql(sql)
            r = result.fetchone()
        except:
            logger.error("Could not retrieve data with: %s", sql)
            return False
        if r == None:
            return False 
        try :
            jo = r[5]
            d = json.loads(jo)
        except:
            logger.error("Converting from JSON went wrong!") 
            return False 
        return d
        
    def set_cached_record(self):
        #
        # store self in the cache database
        # 
        cdb = self.odoo_info.cache_db
        if cdb == False: 
            return 
        self.store_in_sqlite(cdb)
