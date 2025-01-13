# 
# OdooProduct
#
# Odoo does "weird" (read I do not understand) things with product and product templates
# ref 1: https://www.odoo.com/forum/help-1/product-template-vs-product-product-94430
# ref 2: https://www.odoo.com/documentation/user/10.0/ecommerce/managing_products/variants.html
# ref 3: https://stackoverflow.com/questions/50014713/product-and-product-template-in-odoo-10
#
# at RW we need no variants to both tables are the "same"
# 
# Gert Wijsman
# January 2025
#

import logging
from .OdooObject import OdooObject 
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OdooProduct(OdooObject, SqliteObject):

    def __init__(self, odoo_info, id, newvalue=None):
        if newvalue != None: 
            logger.debug("Init product: %i and new value: %s", id, newvalue)
            self.product = {'name': newvalue, 'id': id, 'active': True, 'parent_id': False}
            self.id = id
            self.odoo_info = odoo_info
        else: 
            logger.debug("Init product: %i", id)
            super().__init__(odoo_info, id) 
            self.product = self.get_from_odoo()
            if type(self.product) is list: 
                self.product = self.product[0] 
            self.initialize_new_fields()
        self.set_cached_record() 

    def data(self):
        return self.product

    def external_name(self):
        return "product" 

    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('product.template', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def sqlite_table_name(self):
        return 'product'

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
            result = odoo_info.kw_create('product.template', domain)
            self.data()['toid2025'] = result
            self.data()['migrated2025'] = True
            self.set_cached_record() 
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False
        return result 

    def alfa_keys(self):
        return [
            'id',
            'name', 
            'display_name',
            'active',
            'invoice_policy',
            'sale_ok',
            'purchase_ok',
            'recurring_invoice', 
            'category_id', 
            'description', 

        ]

    def boolean_field_keys(self):
        return [
            'active',
        ]
    def one_join_keys(self):
        return [
#            'product_tmpl_id'
        ]

    def multi_join_keys(self):
        return [
            'product_variant_ids'
        ]

    def write_to_database_keys(self):
        return [
            'name',
            'invoice_policy',
            #'list_price',
            #'taxes_id',
            #'standard_price', 
            #'categ_id',
            #'default_code',
            #'barcode', 
            'sale_ok',
            'purchase_ok',
            'recurring_invoice', 
            'category_id', 
            'description', 
        ]

    def initialize_new_fields(self):
        self.data()['invoice_policy'] = False
        self.data()['recurring_invoice'] = False 
        self.data()['category_id'] = False 

    def delete_from_database(self, odoo_info):
        domain = [[['id', '=', self.id]]]
        domain = [[self.id]]
        print(domain)
        result = odoo_info.kw_delete('product.template', domain)
        print("Result delete: ", result)
        return result 
