#
# SqliteDB
#
# Gert Wijsman
# Dec 2024
#
import logging
import sqlite3

logger = logging.getLogger(__name__)

class SqliteDB():

    def __init__(self, databasefile):
        logger.info("Start db for: %s", databasefile)
        self.con = sqlite3.connect(databasefile)
        logger.info("opened with lib: %s", sqlite3.version)

    def close(self):
        self.con.close()
    
    def exec_sql(self, sql, data=()):
        cur = self.con.cursor()
        result = cur.execute(sql, data)
        self.con.commit() 
        return result
    
    def initialize_db(self):
        for tablename in ['customer', 'contact', 'country', 'state']:
            sql = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + \
            """
            id       INTEGER  PRIMARY KEY,
            name     TEXT     NOT NULL, 
            migrated BOOLEAN  NOT NULL DEFAULT 0,
            reason   TEXT     NOT NULL DEFAULT '',
            to_id    INTERGER NOT NULL DEFAULT 0,
            json     TEXT     NOT NULL DEFAULT ''
            );
            """
            self.exec_sql(sql) 
