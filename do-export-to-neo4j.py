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
from package.ImportLogging import setup_logging 
from package.neo4j.Neo4jDB import Neo4jDB

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

    odoo_info = OdooInfo(db, username, password, host)
    logger.debug("DB connection: %s", odoo_info)
    
    odoo_issues = OdooIssues(odoo_info)

    neo4jdb = Neo4jDB() 
    
    for issue in odoo_issues: 
        logger.info(issue)
        # issue.debug_dump(False)
        # issue.debug_dump()
        issue.write_to_neo4j(neo4jdb) 
        # exit()
        # break 
    logger.info("ODOO Export done.")
    neo4jdb.close() 
        
if __name__ == "__main__":
    main()
