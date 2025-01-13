#
# OdooSalesOrder
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
from .OdooAnalyticAccount import OdooAnalyticAccount
from .OdooProject import OdooProject 
from .OdooInvoice import OdooInvoice 
from .OdooSalesOrderLine import OdooSalesOrderLine
from .OdooFinders import OdooFinders
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OdooSalesOrder(OdooObject, SqliteObject):
    def __init__(self, odoo_info, id):
        logger.debug("Init SalesOrder: %i", id)
        super().__init__(odoo_info, id) 
        self.sales_order = self.get_from_odoo()
        if type(self.sales_order) == list:
            self.sales_order = self.sales_order[0]
        self.folder = False
        self.attachments = False
        self.set_cached_record() 

    def data(self):
        return self.sales_order

    def external_name(self):
        return "SalesOrder" 
        
    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('sale.order', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def alfa_keys(self):
        return [
            'id',
            'display_name',
            'name',
            '__last_update', 
            'origin',
            'client_order_ref',
            'date_order', 
            'note', 
        ]

    def boolean_field_keys(self):
        return [
            'is_auth',
        ]
    
    def one_join_keys(self):
        return [
            'opportunity_id',
            'partner_id',
            'product_id',
            'user_id',
            'currency_id', 
            'fiscal_position', 
            'payment_term', 
            'order_type_id', 
            'pricelist_id',
            'section_id',
            'project_id', 
            'state',
        ]

    def multi_join_keys(self):
        return [
            'invoice_ids',
            'order_line'
        ]

    def write_to_database_keys(self):
        return [
            'name',
            'state', 
            'partner_id', 
            'date_order',
            'order_line', 
            'note', 
        ]

    def write_to_database(self, odoo_info):
        self.correct_text_fields() 
        field_list = self.compile_field_list() 
        #try:
        domain = [field_list] 
        result = odoo_info.kw_create('sale.order', domain)
        self.data()['toid2025'] = result
        self.data()['migrated2025'] = True
        self.create_order_lines(odoo_info, result)
        self.set_cached_record() 
        #self.debug_dump()
        return result 
        #except Exception as v:
        #    logger.error("ERROR AUTHENTICATING %s", v)
        #    return False

    def delete_from_database(self, odoo_info):
        #try:
        domain = [[['id', '=', self.id]]]
        domain = [[self.id]]
        print(domain)
        result = odoo_info.kw_delete('res.sales_order', domain)
        print("Result delete: ", result)
        return result 

    def calculate_one_join_field(self, key, value):
        if key == 'parent_id':
            return value
        elif key == 'partner_id':
            if value is False:
                return False 
            #OdooFinders.show_finders() 
            partnerfinder = OdooFinders.get_finder('partner')
            id = partnerfinder.get_partner_id_for_id(value[0])
            return id 
        elif key == 'state':
            if value in ['draft']:
                return 'draft'
            elif value in ['sent', 'waiting_date', 'manual', 'progress', 'shipping_except', 'invoice_except']:
                return 'sent'
            elif value == 'done':
                return 'sale'
            elif value == 'cancel':
                return 'cancel'
            else:
                logger.error("Unexpected value for state: %s", value)
        return super().calculate_one_join_field(key, value)

    def calculate_multi_join_field(self, key, value):
        # return a new list of ids for the new db
        # return false if noting to do 
        if key is 'category_id':
            nvalue = []
            categoryfinder = OdooFinders.get_finder('category')
            for oid in value:
                nid = categoryfinder.get_category_id_for_id(oid)
                if not nid is False:
                    nvalue.append(nid)
            nvalue.append(categoryfinder.get_migration_category())
            return nvalue
        elif key == 'order_line':
            return False 
        return False

    def create_order_lines(self, odoo_info, order_id):
        osolids = self.data()['order_line']
        nsolids = []
        for osolid in osolids:
            sol = OdooSalesOrderLine(self.odoo_info, osolid)
            sol.data()['order_id'] = order_id
            #sol.debug_dump()
            nlid = sol.write_to_database(odoo_info)
            nsolids.append(nlid)
        self.data()['new_sales_order_line_ids'] = nsolids
        return nsolids

    def sqlite_table_name(self):
        return 'sales_order'

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
        text = self.data()['note']
        if text != False:
            s = text.split('\n')
            new_text = text.replace('\n', '<br>')
            self.data()['note'] = new_text

    def report(self):
        for f in [
            'name',
            'state',
            'active',
            'parent_id',
        ]:
            print(self.data()[f])

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
