#
# OdooPartner
#
# wrapper with functionality for the Parent
#
# 
# Gert Wijsman
# November 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging
from .OdooHTMLParser import OdooHTMLParser
#from .OdooAttachments import OdooAttachments
#from .OdooAttachment import OdooAttachment
#from ..neo4j.Neo4jDB import Neo4jDB
#from pypher import Pypher, __
from .OdooObject import OdooObject 
from .OdooFinders import OdooFinders
from ..sqlite.SqliteObject import SqliteObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OdooPartner(OdooObject, SqliteObject):
    def __init__(self, odoo_info, id):
        logger.debug("Init Partner: %i", id)
        super().__init__(odoo_info, id) 
        self.partner = self.get_from_odoo()
        if type(self.partner) == list:
            self.partner = self.partner[0]
        self.folder = False
        self.attachments = False
        self.set_cached_record() 

    def data(self):
        return self.partner

    def external_name(self):
        return "Partner" 
        
    def get_from_odoo(self):
        cr = self.get_cached_record()
        if cr != False:
            return cr 
        try:
            return self.odoo_info.kw_read_result('res.partner', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def alfa_keys(self):
        return [
            'id',
            'display_name',
            'name',
            'email',  
            'street',
            'street2',
            'street3',
            'zip',
            'website',
            'city',
            '__last_update', 
            'sale_order_count', 
            'supplier_invoice_count',
            'total_invoiced',
            'task_count',
            'issue_count'
        ]

    def boolean_field_keys(self):
        return [
            'active',
            'is_company',
            'supplier',
            'employee'
        ]
    
    def one_join_keys(self):
        return [
            'company_id',
            'parent_id',
            'state_id',
            'country_id',
            'title',
        ]

    def multi_join_keys(self):
        return [
            'child_ids',
            'contract_ids',
            'opportunity_ids',
            'sale_order_ids',
            'invoice_ids',
            'task_ids',
            'interest_ids',
            'category_id',
        ]


    def write_header_to_csv(self, f):
            f.write(
                'id,' + 
                'display_name,' + 
                'active,' + 
                '__last_update,' + 
                'is_company,' + 
                'supplier,' + 
                'sale_order_count,' + 
                'supplier_invoice_count,' + 
                'total_invoiced,' + 
                'task_count,' + 
                'issue_count,' +
                'child_ids,' + 
                'contract_ids,' +
                'opportunity_ids,' +
                'invoice_ids,' +
                'task_ids,' +
                'company_id,' + 
                'parent_id,' +
                'country_id'
            )
            f.write('\n')
        
    def write_info_to_csv(self, f):
        if not self.is_valid():
            f.write("no access to issue")
            return
        for i_key in [
                'id', 
                'display_name',
                'active',
                '__last_update', 
                'is_company',
                'supplier', 
                'sale_order_count',
                'supplier_invoice_count', 
                'total_invoiced', 
                'task_count',
                'issue_count',
                'child_ids',
                'contract_ids',
                'opportunity_ids',
                'invoice_ids',
                'task_ids',
                'company_id',
                'parent_id',
                'country_id'
        ]:
            if i_key in ['company_id', 'parent_id', 'country_id']:
                s = self.one_relation_value(i_key)
                f.write(str(s))
            elif i_key in ['child_ids', 'contract_ids', 'opportunity_ids', 'invoice_ids','task_ids']:
                c = self.count_relation_occurrence(i_key)
                f.write(str(c))
            else:
                f.write(str(self.customer[i_key]))
            if i_key == 'country_id':
                f.write('\n')
            else:
                f.write(",")
            
    def one_relation_value(self, i_key):
        v = self.customer[i_key]
        if v == False:
            return 0
        else:
            return v[1]

    def count_relation_occurrence(self, i_key):
        v = self.customer[i_key]
        return len(v) 

    def write_to_database_keys(self):
        # please look at the child definition 
        return [
            'name',
            'email',  
            'active',
            'is_company',
            'street',
            'street2',
            'zip',
            'city', 
            'website', 
            'lang',
            'title', 
#            'supplier', 
#            'company_id',
#            'parent_id'
            'country_id',
            'country_code', 
        # please look at the child definition!
        ]

    def write_to_database(self, odoo_info):
        self.correct_comment_field() 
        field_list = self.compile_field_list() 
        #try:
        domain = [field_list] 
        # print(domain)
        result = odoo_info.kw_create('res.partner', domain)
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
        result = odoo_info.kw_delete('res.partner', domain)
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
        if key == 'category_id':
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

    # def write_to_text_file(self, folder, withAttachments=False):
    #     # folder is the folder to write the file to
    #     # subfoder div 100?!? (only if needed)
    #     self.folder = folder
    #     self.attachments = withAttachments 
    #     filename = self.folder + '/' + str(self.id) + '.txt'
    #     try:
    #         f = open(filename, 'w') # replace with 'x' later (when no overwriting needed!) 
    #     except Exception:
    #         logger.error("Failed opening file: %s", filename)
    #         return 
    #     try:
    #         self.write_info(f)
    #     except Exception as v:
    #         logger.error("Failed writing to file: %s", v) 
    #     f.close() 
    #     logger.info("created file: %s", filename)

    # def write_info(self, f):
    #     i = self.issue
    #     if i == False:
    #         f.write("no access to issue")
    #         return
    #     for i_key in [
    #             'id', 
    #             'display_name',
    #             'product',  
    #             'name',
    #             'message_summary',
    #             'partner_id',
    #             'analytic_account_id',
    #             'user_id',
    #             'priority',
    #             'issue_stage_id',
    #             'email_from',
    #             'message_ids']:
    #         f.write(i_key)
    #         f.write(": ")
    #         f.write(str(self.issue[i_key]))
    #         f.write('\n')
    #     self.write_description(f)
    #     self.write_messages(f)
    #     if self.attachments:
    #         self.save_attachments_with_issue(f)

    # def write_description(self, f):
    #     d = self.issue['description']
    #     f.write('\n')
    #     f.write('\n')
    #     f.write('Description: ') 
    #     f.write('\n')
        
    #     ohp = OdooHTMLParser()
    #     ohp.feed(d)
    #     ohp.close() 
    #     f.write(ohp.text)
        
    #     f.write('\n')
    #     f.write('\n')

    # def write_messages(self, f):
    #     msgids = self.issue['message_ids']
    #     f.write('Messages: ') 
    #     f.write('\n')
    #     for id in msgids:
    #         msg = OdooMessage(self, id)
    #         msg.write_on(f)
    #     f.write('\n')

    # def save_attachments_with_issue(self, f):
    #     logger.debug("Save Attachments")
    #     l = OdooAttachments(self.odoo_info, self)
    #     for a in l:
    #         attachment = OdooAttachment(self.odoo_info, self, a)
    #         attachment.save()
    #         attachment.add_url(f)

    # def domain_for_attachments(self):
    #     # d = [[['res_model', '=', 'project.issue'], ['res_id', '=', 3998]]]
    #     d = [[['res_model', '=', 'project.issue'], ['res_id', '=', self.id]]]
    #     return d

    # def write_to_neo4j(self, neo4jdb):
    #     if not self.is_valid():
    #         logger.warning("Issue invalid! (%i)", self.id)
    #         return False 
    #     logger.info("Create issue in neo4j: %i", self.id)
    #     query, values = self.build_neo4j_query_and_values()
    #     with neo4jdb.session() as session:
    #         try:
    #             result = session.run(query, values)
    #             node_issue = result.single()
    #         except Exception as v:
    #             logger.error("ERROR %i, %s", self.id, v)
    #             session.close() 
    #             return 
    #         session.close()
    #     self.join_messages_to_issue(neo4jdb)
    #     self.join_attachments_to_issue(neo4jdb) 
            
    # def build_neo4j_query_and_values(self):
    #     q = Pypher()
    #     q.MERGE.node('i', 'Issue', Number = self.id).SET(
    #         __.i.__Name__      == self.issue['display_name'],
    #         __.i.__Product__   == self.issue['product'], 
    #         __.i.__Priority__  == self.issue['priority'],
    #         __.i.__EmailFrom__ == self.issue['email_from']
    #     )
    #     self.join_partner_to_query(q)
    #     self.join_analytic_account_to_query(q)
    #     self.join_user_to_query(q)
    #     self.join_issue_stage_to_query(q)
    #     self.join_description_to_query(q)
    #     cypher = str(q)
    #     params = q.bound_params
    #     #print("Pypher: ", cypher)
    #     #print("  with: ", params)
    #     return cypher, params 

    # def join_partner_to_query(self, query):
    #     odoo_partner = self.issue['partner_id']
    #     if odoo_partner == False:
    #         return
    #     #print('PA: ', odoo_partner)
    #     query.MERGE.node('part', 'Partner', number = odoo_partner[0]).SET(
    #         __.part.__name__ == odoo_partner[1]
    #         )
    #     query.MERGE.node('i').rel_out(labels='PARTNER').node('part')

    # def join_analytic_account_to_query(self, query):
    #     odoo_analytic_account = self.issue['analytic_account_id']
    #     if odoo_analytic_account == False:
    #         return
    #     #print('AA: ', odoo_analytic_account) 
    #     query.MERGE.node('aa', 'AnalyticAccount', number = odoo_analytic_account[0]).SET(
    #         __.aa.__name__ == odoo_analytic_account[1]
    #         )
    #     query.MERGE.node('i').rel_out(labels='ANALYTICACCOUNT').node('aa')
    
    # def join_user_to_query(self, query):
    #     odoo_user = self.issue['user_id']
    #     if odoo_user == False:
    #         return
    #     #print('US: ', odoo_user)
    #     query.MERGE.node('u', 'User', number = odoo_user[0]).SET(
    #         __.u.__name__ == odoo_user[1]
    #         )
    #     query.MERGE.node('i').rel_out(labels='USER').node('u')
        
    # def join_issue_stage_to_query(self, query):
    #     odoo_issue_stage = self.issue['issue_stage_id']
    #     if odoo_issue_stage == False:
    #         return
    #     #print('ST: ', odoo_issue_stage)
    #     query.MERGE.node('st', 'Stage', number = odoo_issue_stage[0]).SET(
    #         __.st.__name__ == odoo_issue_stage[1]
    #         )
    #     query.MERGE.node('i').rel_out(labels='STAGE').node('st')
        
    # def join_description_to_query(self, query):
    #     odoo_description = self.issue['description']
    #     if odoo_description == False:
    #         return

    #     ohp = OdooHTMLParser()
    #     ohp.feed(odoo_description)
    #     ohp.close() 
    #     t = ohp.text

    #     #print('DE: ', t)
    #     #print('--')
    #     query.MERGE.node('de', 'Description', number = self.id).SET(
    #         __.de.__description__ == t
    #         )
    #     query.MERGE.node('i').rel_out(labels='DESCRIPTION').node('de')

    # def join_messages_to_issue(self, neo4jdb):
    #     msgids = self.issue['message_ids']
    #     #print('MSGS: ', msgids) 
    #     for id in msgids:
    #         msg = OdooMessage(self, id)
    #         msg.join_to_issue(neo4jdb)
    #         # break 

    # def join_attachments_to_issue(self, neo4jdb):
    #     logger.debug("Join Attachments")
    #     l = OdooAttachments(self.odoo_info, self)
    #     #print('ATTS: ', l) 
    #     for a in l:
    #         attachment = OdooAttachment(self.odoo_info, self, a)
    #         attachment.join_to_issue(neo4jdb)

            
        
    # the attachments with the issue can be found by: 
    # resource model = project.issue
    # resource id = de id van het issue
    # (resource name is teh title string of the issue) 
    
    # table: ir.attachment
    # field: res_model (char)
    # field: res_id (int) 

    def sqlite_table_name(self):
        return 'partner'

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
