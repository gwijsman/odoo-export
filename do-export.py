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
from dotenv import load_dotenv
from odoo.OdooInfo import OdooInfo
from odoo.OdooIssues import OdooIssues
from odoo.OdooIssue import OdooIssue

def main():
    load_dotenv()
    
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USERNAME')
    password = os.getenv('ODOO_PASSWORD')
    
    host = os.getenv('ODOO_HOST')
    url = "https://" + host + "/xmlrpc/2/"
    
    odoo_info = OdooInfo(db, username, password, host)
    print(odoo_info)
    
    odoo_issues = OdooIssues(odoo_info)
    
    for issue in odoo_issues: 
        print(issue)
        
if __name__ == "__main__":
    print("Starting do-export...")
    main()
    print("do-export done.")
