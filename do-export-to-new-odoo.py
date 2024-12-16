#
# new odoo
#
# Gert Wijsman
# August 2024
#
# inspriation:
# https://www.odoo.com/documentation/8.0/api_integration.html
#

import os
import logging
from dotenv import load_dotenv
from package.odoo.OdooInfo import OdooInfo
from package.migration.Migration import Migration
from package.ImportLogging import setup_logging 

logger = logging.getLogger(__name__)

def main():
    load_dotenv()
    setup_logging()
    logger.info("Starting ODOO Export...")
    
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USERNAME')
    password = os.getenv('ODOO_PASSWORD')
    host = os.getenv('ODOO_HOST')

    db_out = os.getenv('ODOO_DB_OUT')
    username_out = os.getenv('ODOO_USERNAME_OUT')
    password_out = os.getenv('ODOO_PASSWORD_OUT')
    host_out = os.getenv('ODOO_HOST_OUT')

    outputfolder = os.getenv('TEXT_OUTPUT_FOLDER')

    # set to None for no limit: 
    debug_limit = None
    debug_limit = 250
    odoo_in_info = OdooInfo(db, username, password, host, debug_limit)
    logger.debug("DB in connection: %s", odoo_in_info)
    odoo_out_info = OdooInfo(db_out, username_out, password_out, host_out)
    logger.debug("DB out connection: %s", odoo_out_info)

    migration = Migration(odoo_in_info, odoo_out_info)
    migration.do() 
        
    logger.info("ODOO Export done.")

if __name__ == "__main__":
    main()
