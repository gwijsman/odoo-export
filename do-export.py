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
from odoo.OdooInfo import OdooInfo
from odoo.OdooIssues import OdooIssues
from odoo.OdooIssue import OdooIssue
from ImportLogging import setup_logging 

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
    
    odoo_issues = OdooIssues(odoo_info)
    
    for issue in odoo_issues: 
        print(issue)
        # issue.debug_dump(False)
        # issue.debug_dump()
        issue.write_to_text_file(outputfolder)
        # exit()
    logger.info("ODOO Export done.")
        
if __name__ == "__main__":
    main()
