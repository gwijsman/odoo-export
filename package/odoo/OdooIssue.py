#
# OdooIssue
#
# wrapper with functionality specific for the Issue itself
#
# Main purpose is writing the issue "readable" to file
# The LLM should be able to analyse these txt files
# and translate them to a vector graph with help of langchain 
# 
# Gert Wijsman
# August 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging
from .OdooMessage import OdooMessage 
from .OdooHTMLParser import OdooHTMLParser
from .OdooAttachments import OdooAttachments
from .OdooAttachment import OdooAttachment
from ..neo4j.Neo4jDB import Neo4jDB
from pypher import Pypher, __

logger = logging.getLogger(__name__)

class OdooIssue:
    def __init__(self, odoo_info, id):
        logger.debug("Init issue: %i", id)
        self.id = id
        self.odoo_info = odoo_info
        self.issue = self.get_from_odoo()
        self.folder = False
        self.attachments = False
        if self.issue is False:
            return 
        self.issue['product'] = self.product()
        
    def __str__(self):
        if self.issue != False:
            title = self.issue['display_name']
        else:
            title = "empty/no-access"
        return f"OdooIssue with id: {self.id} - {title}"
        
    def get_from_odoo(self):
        try:
            return self.odoo_info.kw_read_result('project.issue', [self.id])
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False

    def debug_dump(self, with_keys=True):
        if self.issue == False:
            print(self)
            return
        print("==========", self.id)
        if with_keys:
            for i_key in self.issue.keys():
                print(i_key)
        print("==========", self.id)
        print(self)
        print("==========", self.id)
        for i_key in [
                'display_name',
                'product',
                'name', 
                'partner_id',
                'analytic_account_id',
                'user_id',
                'priority',
                'issue_stage_id',
                'email_from',
                'message_ids']:
            print(i_key, ": ", self.issue[i_key])
        print("==========", self.id)
        
    def product(self):
        if self.issue == False:
            return 'Unknown'
        if self.issue['analytic_account_id'] is False:
            return 'Unknown'
        analytic_account = self.issue['analytic_account_id'][1]
        if 'SWEG' in analytic_account:
            return 'SWEG'
        elif 'Diagnostics'in analytic_account:
            return 'Diagnostics'
        elif ('Water Office' in analytic_account) or ('WO'in analytic_account):
            return 'Water Office'
        else:
            return 'Unknown'

    def is_valid(self):
        return self.issue != False 
        
    def write_to_text_file(self, folder, withAttachments=False):
        # folder is the folder to write the file to
        # subfoder div 100?!? (only if needed)
        self.folder = folder
        self.attachments = withAttachments 
        filename = self.folder + '/' + str(self.id) + '.txt'
        try:
            f = open(filename, 'w') # replace with 'x' later (when no overwriting needed!) 
        except Exception:
            logger.error("Failed opening file: %s", filename)
            return 
        try:
            self.write_info(f)
        except Exception as v:
            logger.error("Failed writing to file: %s", v) 
        f.close() 
        logger.info("created file: %s", filename)

    def write_info(self, f):
        i = self.issue
        if i == False:
            f.write("no access to issue")
            return
        for i_key in [
                'id', 
                'display_name',
                'product',  
                'name',
                'message_summary',
                'partner_id',
                'analytic_account_id',
                'user_id',
                'priority',
                'issue_stage_id',
                'email_from',
                'message_ids']:
            f.write(i_key)
            f.write(": ")
            f.write(str(self.issue[i_key]))
            f.write('\n')
        self.write_description(f)
        self.write_messages(f)
        if self.attachments:
            self.save_attachments_with_issue(f)

    def write_description(self, f):
        d = self.issue['description']
        f.write('\n')
        f.write('\n')
        f.write('Description: ') 
        f.write('\n')
        
        ohp = OdooHTMLParser()
        ohp.feed(d)
        ohp.close() 
        f.write(ohp.text)
        
        f.write('\n')
        f.write('\n')

    def write_messages(self, f):
        msgids = self.issue['message_ids']
        f.write('Messages: ') 
        f.write('\n')
        for id in msgids:
            msg = OdooMessage(self, id)
            msg.write_on(f)
        f.write('\n')

    def save_attachments_with_issue(self, f):
        logger.debug("Save Attachments")
        l = OdooAttachments(self.odoo_info, self)
        for a in l:
            attachment = OdooAttachment(self.odoo_info, self, a)
            attachment.save()
            attachment.add_url(f)

    def domain_for_attachments(self):
        # d = [[['res_model', '=', 'project.issue'], ['res_id', '=', 3998]]]
        d = [[['res_model', '=', 'project.issue'], ['res_id', '=', self.id]]]
        return d

    def write_to_neo4j(self, neo4jdb):
        if not self.is_valid():
            logger.warning("Issue invalid! (%i)", self.id)
            return False 
        logger.info("Create issue in neo4j: %i", self.id)
        query, values = self.build_neo4j_query_and_values()
        with neo4jdb.session() as session:
            try:
                result = session.run(query, values)
                node_issue = result.single()
            except Exception as v:
                logger.error("ERROR %i, %s", self.id, v)
                session.close() 
                return 
            session.close()
        self.join_messages_to_issue(neo4jdb)
        self.join_attachments_to_issue(neo4jdb) 
            
    def build_neo4j_query_and_values(self):
        q = Pypher()
        q.MERGE.node('i', 'Issue', Number = self.id).SET(
            __.i.__Name__      == self.issue['display_name'],
            __.i.__Product__   == self.issue['product'], 
            __.i.__Priority__  == self.issue['priority'],
            __.i.__EmailFrom__ == self.issue['email_from']
        )
        self.join_partner_to_query(q)
        self.join_analytic_account_to_query(q)
        self.join_user_to_query(q)
        self.join_issue_stage_to_query(q)
        self.join_description_to_query(q)
        cypher = str(q)
        params = q.bound_params
        #print("Pypher: ", cypher)
        #print("  with: ", params)
        return cypher, params 

    def join_partner_to_query(self, query):
        odoo_partner = self.issue['partner_id']
        if odoo_partner == False:
            return
        #print('PA: ', odoo_partner)
        query.MERGE.node('part', 'Partner', number = odoo_partner[0]).SET(
            __.part.__name__ == odoo_partner[1]
            )
        query.MERGE.node('i').rel_out(labels='PARTNER').node('part')

    def join_analytic_account_to_query(self, query):
        odoo_analytic_account = self.issue['analytic_account_id']
        if odoo_analytic_account == False:
            return
        #print('AA: ', odoo_analytic_account) 
        query.MERGE.node('aa', 'AnalyticAccount', number = odoo_analytic_account[0]).SET(
            __.aa.__name__ == odoo_analytic_account[1]
            )
        query.MERGE.node('i').rel_out(labels='ANALYTICACCOUNT').node('aa')
    
    def join_user_to_query(self, query):
        odoo_user = self.issue['user_id']
        if odoo_user == False:
            return
        #print('US: ', odoo_user)
        query.MERGE.node('u', 'User', number = odoo_user[0]).SET(
            __.u.__name__ == odoo_user[1]
            )
        query.MERGE.node('i').rel_out(labels='USER').node('u')
        
    def join_issue_stage_to_query(self, query):
        odoo_issue_stage = self.issue['issue_stage_id']
        if odoo_issue_stage == False:
            return
        #print('ST: ', odoo_issue_stage)
        query.MERGE.node('st', 'Stage', number = odoo_issue_stage[0]).SET(
            __.st.__name__ == odoo_issue_stage[1]
            )
        query.MERGE.node('i').rel_out(labels='STAGE').node('st')
        
    def join_description_to_query(self, query):
        odoo_description = self.issue['description']
        if odoo_description == False:
            return

        ohp = OdooHTMLParser()
        ohp.feed(odoo_description)
        ohp.close() 
        t = ohp.text

        #print('DE: ', t)
        #print('--')
        query.MERGE.node('de', 'Description', number = self.id).SET(
            __.de.__description__ == t
            )
        query.MERGE.node('i').rel_out(labels='DESCRIPTION').node('de')

    def join_messages_to_issue(self, neo4jdb):
        msgids = self.issue['message_ids']
        #print('MSGS: ', msgids) 
        for id in msgids:
            msg = OdooMessage(self, id)
            msg.join_to_issue(neo4jdb)
            # break 

    def join_attachments_to_issue(self, neo4jdb):
        logger.debug("Join Attachments")
        l = OdooAttachments(self.odoo_info, self)
        #print('ATTS: ', l) 
        for a in l:
            attachment = OdooAttachment(self.odoo_info, self, a)
            attachment.join_to_issue(neo4jdb)

            
        
# the attachments with the issue can be found by: 
# resource model = project.issue
# resource id = de id van het issue
# (resource name is teh title string of the issue) 

# table: ir.attachment
# field: res_model (char)
# field: res_id (int) 
