#
# OdooSalesOrderLine
#
#
# 
# Gert Wijsman
# Januari 2025
#
# inspriation:
# I love Object Oriented programming 
#

import logging
from .OdooHTMLParser import OdooHTMLParser
from .OdooObject import OdooObject 
from .OdooFinders import OdooFinders
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OdooSalesOrderLine(OdooObject, SqliteObject):
    def __init__(self, odoo_info, id):
        logger.debug("Init SalesOrderLine: %i", id)
        super().__init__(odoo_info, id) 
        self.sales_order_line = self.get_from_odoo()
        if type(self.sales_order_line) == list:
            self.sales_order_line = self.sales_order_line[0]
        self.folder = False
        self.attachments = False
        self.set_cached_record() 

    def data(self):
        return self.sales_order_line

    def external_name(self):
        return "SalesOrderLine" 
        
    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('sale.order.line', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def alfa_keys(self):
        return [
            'id',
            'display_name',
            'name',
            '__last_update', 
            'state',
            'product_uom_qty',
            'price_unit',
            'purchase_price',
            'discount', 
            'price_subtotal', 
        ]

    def boolean_field_keys(self):
        return [
        ]
    
    def one_join_keys(self):
        return [
            'product_uom',
            'product_id',
            'tax_id',
        ]

    def multi_join_keys(self):
        return [
            'invoice_lines',
        ]

    def write_to_database_keys(self):
        return [
            'name',
            'order_id',
            'product_id', 
            'product_uom',
            'tax_id',
            'state',
            'product_uom_qty',
            'price_unit',
            'purchase_price',
            'discount', 
            'price_subtotal', 
        ]

    def write_to_database(self, odoo_info):
        field_list = self.compile_field_list() 
        domain = [field_list] 
        result = odoo_info.kw_create('sale.order.line', domain)
        self.data()['toid2025'] = result
        self.data()['migrated2025'] = True
        self.set_cached_record() 
        return result 

    def delete_from_database(self, odoo_info):
        #try:
        domain = [[['id', '=', self.id]]]
        domain = [[self.id]]
        print(domain)
        result = odoo_info.kw_delete('res.sales_order_line', domain)
        print("Result delete: ", result)
        return result 

    def calculate_one_join_field(self, key, value):
        if value is False:
            return False 
        if key == 'tax_id':
            #OdooFinders.show_finders() 
            taxfinder = OdooFinders.get_finder('tax')
            id = taxfinder.get_tax_id_for_id(value[0])
            return id 
        elif key == 'product_id':
            #OdooFinders.show_finders() 
            productfinder = OdooFinders.get_finder('product')
            id = productfinder.get_product_id_for_id(value[0])
            return id 
        elif key == 'product_uom': 
            #OdooFinders.show_finders() 
            uomfinder = OdooFinders.get_finder('uom')
            id = uomfinder.get_uom_id_for_id(value[0])
            return id 
        return super().calculate_one_join_field(key, value)

#    def calculate_multi_join_field(self, key, value):
#        # return a new list of ids for the new db
#        # return false if noting to do 
#        if key is 'category_id':
#            nvalue = []
#            categoryfinder = OdooFinders.get_finder('category')
#            for oid in value:
#                nid = categoryfinder.get_category_id_for_id(oid)
#                if not nid is False:
#                    nvalue.append(nid)
#            nvalue.append(categoryfinder.get_migration_category())
#            return nvalue
#        return False

    def sqlite_table_name(self):
        return 'sales_order_line'

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
    
    def correct_text_fields(self):
        text = self.data()['description']
        if text != False:
            s = text.split('\n')
            new_text = text.replace('\n', '<br>')
            self.data()['description'] = new_text

    def write_info_to_csv(self, f):
        if not self.is_valid():
            f.write("no access to issue")
            return
        for i_key in [
                'id',
                'display_name',
                'name',
                '__last_update', 
                'state',
                'is_auth',
                'opportunity_id',
                'partner_id',
                'product_id',
                'user_id',
                'project_id',
                'invoice_ids',
                'newline'
        ]:
            if i_key == 'newline':
                f.write('\n')
                continue 
            elif i_key in ['opportunity_id', 'partner_id', 'product_id', 'user_id', 'project_id']:
                s = self.one_relation_value(i_key)
                f.write(str(s))
            elif i_key in ['invoice_ids']:
                s = self.relation_info(i_key)
                f.write(s)
            else:
                f.write(str(self.data()[i_key]))
            f.write(",")

    def one_relation_value(self, key):
        v = self.data()[key]
        if v == False:
            return "-,-"
        elif key in ['project_id']:
            aa = OdooAnalyticAccount(self.odoo_info, v[0])
            s = str(aa.data()['name'])
            s += ','
            s += str(aa.data()['state'])
            return s
        else:
            return str(v[0]) + ',' + v[1]

    def relation_info(self, key):
        if key == 'invoice_ids':
            return self.invoice_info()
        c = len(self.data()[key])
        return str(c) 
    
    def invoice_info(self):
        v = self.data()['invoice_ids']
        if len(v) == 0:
            return 'no invoice,-,-,-' 
        for id in v:
            i = OdooInvoice(self.odoo_info, id)
            if i.data()['state'] == 'canceled':
                continue 
            r = i.data()['name'] # fun not reference! 
            n = i.data()['internal_number']
            t = i.data()['amount_total']
            return str(id) + ',' + str(r) + ',' + str(n) + ',' + str(t) 
