#
# delete added record in test database
#
# Gert Wijsman
# December 2024
#

import os
import json 

from dotenv import load_dotenv
from package.odoo.OdooInfo import OdooInfo
from package.odoo.OdooCustomers import OdooCustomers
from package.odoo.OdooContacts import OdooContacts 
from package.odoo.OdooCustomer import OdooCustomer
from package.odoo.OdooContact import OdooContact
from package.sqlite.SqliteDB import SqliteDB

def show_info(odoo_out_info):
    domain = [
        [
            ['is_company', '=', False],
            #['customer', '=', True], 
            #['supplier', '=', False],
            ['active', '=', True],
            #['parent_id', '=', 470],
        ]    
    ]
    print(domain)
    odoo_contacts = OdooContacts(odoo_out_info, domain) 
    for contact in odoo_contacts:
        print(contact)
        jo = json.dumps(contact.data())
        print('=====')
        print(jo)
        print('=====')
        exit()

def delete_customers(odoo_out_info):
    domain = [
        [
            ['is_company', '=', True],
            #['customer', '=', True], 
            #['supplier', '=', False],
            ['active', '=', True],
            #['parent_id', '=', 470],
        ]    
    ]
    print(domain)
    odoo_customers = OdooCustomers(odoo_out_info, domain) 
    for customer in odoo_customers:
        print(customer)
        if customer.id in [1,69]:
            continue 
        print("Delete: ", customer)
        customer.delete_from_database(odoo_out_info) 

def delete_contacts(odoo_out_info):
    domain = [
        [
            ['is_company', '=', False],
            #['customer', '=', True], 
            #['supplier', '=', False],
            ['active', '=', True],
            #['parent_id', '=', 470],
        ]    
    ]
    print(domain)
    odoo_contacts = OdooContacts(odoo_out_info, domain) 
    for contact in odoo_contacts:
        print(contact)
        #jo = json.dumps(contact.data())
        #print('=====')
        #print(jo)
        #print('=====')
        #exit()
        if contact.id in [3, 7, 8]:
            continue 
        print("Delete: ", contact)
        contact.delete_from_database(odoo_out_info) 

def main():
    load_dotenv()
    
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
    # debug_limit = 250
    odoo_in_info = OdooInfo(db, username, password, host, debug_limit)
    odoo_out_info = OdooInfo(db_out, username_out, password_out, host_out)

    sqlitedbfile = os.getenv('SQLITEFILE')
    sdb = SqliteDB(sqlitedbfile)
    sdb.initialize_db()
    odoo_in_info.cache_db = sdb 

    delete_contacts(odoo_out_info)
    delete_customers(odoo_out_info)
    # show_info(odoo_out_info)

if __name__ == "__main__":
    main()
