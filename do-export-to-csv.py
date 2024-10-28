#
# export all issues from odoo with message to txt files
# for usage of GenAI-Stack
# export attachments to a folder
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
from package.odoo.OdooIssues import OdooIssues
from package.odoo.OdooIssue import OdooIssue
from package.odoo.OdooCustomers import OdooCustomers
from package.odoo.OdooCustomer import OdooCustomer
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
    url = "https://" + host + "/xmlrpc/2/"

    outputfolder = os.getenv('TEXT_OUTPUT_FOLDER')
    
    odoo_info = OdooInfo(db, username, password, host)
    logger.debug("DB connection: %s", odoo_info)
    
    odoo_customers = OdooCustomers(odoo_info, [[['is_company', '=', True], ['supplier', '=', False], ['active', '=', True]]])

    filename = outputfolder + '/customers.csv'
    try:
        f = open(filename, 'w') # replace with 'x' later (when no overwriting needed!) 
    except Exception:
        logger.error("Failed opening file: %s", filename)
        return
    #    try:
    odoo_customers.first().write_header_to_csv(f)
    for customer in odoo_customers: 
        logger.debug(customer)
        customer.debug_dump(False)
        # customer.debug_dump()
        customer.write_info_to_csv(f)
        # break
        # exit()
        #except Exception as v:
        #logger.error("Failed writing to file: %s", v) 
        #f.close() 
        #logger.info("created file: %s", filename)
    f.close() 
    logger.info("created file: %s", filename)
    logger.info("ODOO Export done.")
        
if __name__ == "__main__":
    main()
