#
# OdooProject
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
from .OdooFinders import OdooFinders
from .OdooCountryFinder import OdooCountryFinder
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OdooProject(OdooObject, SqliteObject):
    def __init__(self, odoo_info, id):
        logger.debug("Init Project: %i", id)
        super().__init__(odoo_info, id) 
        self.project = self.get_from_odoo()
        if type(self.project) == list:
            self.project = self.project[0]
        self.folder = False
        self.attachments = False
        self.set_cached_record() 

    def data(self):
        return self.project

    def external_name(self):
        return "Project" 
        
    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('project.project', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def alfa_keys(self):
        return [
            'id',
            'display_name',
            'name',
            '__last_update', 
        ]

    def boolean_field_keys(self):
        return [
            'active',
        ]
    
    def one_join_keys(self):
        return [
            'accound_id',
            'partner_id',
            'stage_id',
            'user_id',
        ]

    def multi_join_keys(self):
        return [
        ]

    def write_to_database_keys(self):
        return [
            'name',
            'active',
        ]

    def write_to_database(self, odoo_info):
        self.correct_text_fields() 
        field_list = self.compile_field_list() 
        #try:
        domain = [field_list] 
        # print(domain)
        result = odoo_info.kw_create('project.project', domain)
        self.data()['toid2025'] = result
        self.data()['migrated2025'] = True
        self.set_cached_record() 
        return result 
        #except Exception as v:
        #    logger.error("ERROR AUTHENTICATING %s", v)
        #    return False

    def delete_from_database(self, odoo_info):
        #try:
        domain = [[['id', '=', self.id]]]
        domain = [[self.id]]
        print(domain)
        result = odoo_info.kw_delete('res.project', domain)
        print("Result delete: ", result)
        return result 

    def calculate_one_join_field(self, key, value):
        if key == 'parent_id':
            return value
        elif key == 'country_id':
            if value is False:
                return False 
            #OdooFinders.show_finders() 
            countryfinder = OdooFinders.get_finder('country')
            id = countryfinder.get_country_id_for_id(value[0])
            return id 
        elif key == 'state_id':
            if value is False:
                return False 
            #OdooFinders.show_finders() 
            statefinder = OdooFinders.get_finder('state')
            id = statefinder.get_state_id_for_id(value[0])
            return id 
        elif key == 'title':
            if value is False:
                return False 
            #OdooFinders.show_finders() 
            titlefinder = OdooFinders.get_finder('title')
            id = titlefinder.get_title_id_for_id(value[0])
            return id 
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
        return False

    def correct_comment_field(self):
        comment = self.data()['comment']
        s = comment.split('\n')
        #comment2 = ""
        #for l in s:
        #    comment2 = comment2 + '<p>' + l + '</p>'
        comment2 = comment.replace('\n', '<br>')
        self.data()['comment'] = comment2

    def sqlite_table_name(self):
        return 'project'

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

    def report(self):
        for f in [
            'name',
            'state',
            'active',
        ]:
            print(self.data()[f])
        aaid = self.data()['analytic_account_id'][0]
        aa = OdooAnalyticAccount(self.odoo_info, aaid)
        print(aa)
        print(aa.data()['state'])

    def write_info_to_csv(self, f):
        if not self.is_valid():
            f.write("no access to issue")
            return
        for i_key in [
                'id', 
                'name',
                'active',
                'state',
                '__last_update', 
                'original_date_start',
                'date_start',
                'date',
                'expiry_date',
                'parent_id', 
                'analytic_account_id', 
                'alias_id',
                'alias_parent_model_id',
                'pricelist_id',
                'alias_model_id',
                'alert_writing_hours',
                'sale_order_ids',
                'partner_id',
                'complete_name',
                'newline'
        ]:
            if i_key == 'newline':
                f.write('\n')
                continue 
            elif i_key in ['analytic_account_id', 'parent_id', 'alias_id', 'alias_parent_model_id', 'pricelist_id', 'alias_model_id', 'partner_id']:
                s = self.one_relation_value(i_key)
                f.write(str(s))
            elif i_key in ['sale_order_ids']:
                #c = self.count_relation_occurrence(i_key)
                c = str(len(self.data()[i_key]))
                f.write(str(c))
            else:
                f.write(str(self.data()[i_key]))
            f.write(",")

    def one_relation_value(self, key):
        v = self.data()[key]
        if v == False:
            if key in ['alias_id', 'alias_parent_model_id', 'pricelist_id', 'alias_model_id', 'partner_id']:
                return "-,-"
            else:
                return "-"
        elif key == 'parent_id':
            aa = OdooAnalyticAccount(self.odoo_info, v[0])
            return aa.data()['name'] 
        elif key == 'analytic_account_id':
            aa = OdooAnalyticAccount(self.odoo_info, v[0])
            s = str(aa.data()['name'])
            s += ','
            s += str(aa.data()['state'])
            return s
        elif key in ['alias_id', 'alias_parent_model_id', 'pricelist_id', 'alias_model_id', 'partner_id']:
            return str(v[0]) + ',' + v[1]
        else:
            return v[0]