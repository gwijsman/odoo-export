#
# OdooMessage
#
# wrapper with functionality specific for the Message with the Issue itself
#
# Main purpose is writing the message "readable" to file
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
from .OdooHTMLParser import OdooHTMLParser
from pypher import Pypher, __

logger = logging.getLogger(__name__)

class OdooMessage:
    def __init__(self, parent, id):
        self.id = id
        self.parent = parent 
        self.odoo_info = parent.odoo_info
        self.message = self.get_from_odoo()
        self.folder = parent.folder
        # self.debug_dump(False)
        # self.debug_dump()
        
    def __str__(self):
        if self.is_valid(): 
            title = self.message['display_name']
        else:
            title = "empty/no-access"
        return f"OdooMessage with id: {self.id} - {title}"
        
    def get_from_odoo(self):
        try:
            return self.odoo_info.kw_read_result('mail.message', [self.id])
        except Exception as v:
            self.error("ERROR AUTHENTICATING %s", v)
            return False

    def is_valid(self):
        return self.message != False 

    def debug_dump(self, with_keys=True):
        if self.message == False:
            print(self)
            return
        if with_keys:
            print("==========", self.id)
            print(self)
            print("==========", self.id)
            for i_key in self.message.keys():
                print(i_key, ": ", self.message[i_key])
        else:
            print("==========", self.id)
            print(self)
            print("==========", self.id)
            for i_key in [
                    'display_name',
                    'body',
                    'create_date', 
                    'create_uid']: 
                print(i_key, ": ", self.message[i_key])
        print("==========", self.id)
        
    def write_body(self, f):
        b = self.message['body']
        f.write('\n')
        f.write('\n')
        f.write('Body: ') 
        f.write('\n')
        
        ohp = OdooHTMLParser()
        ohp.feed(b)
        ohp.close()
        f.write(ohp.text)
        f.write('\n')
        f.write('\n')

    def write_on(self, f):
        f.write(self.__str__())
        f.write('\n')
        self.write_body(f)
        f.write('\n')

    def join_to_issue(self, neo4jdb):
        if not self.is_valid():
            logger.warning("Message invalid! (%i)", self.id)
            return False
        if self.skip_me():
            logger.info("Message unnessary! (%i)", self.id)
            return False 
        logger.info("Create message %i in neo4j for issue %i", self.id, self.parent.id)
        #        print(self)
        #        self.debug_dump()
        query, values = self.build_neo4j_query_and_values()
        with neo4jdb.session() as session:
            try:
                result = session.run(query, values)
                node_message = result.single()
            except Exception as v:
                logger.error("ERROR %s", v)
                session.close() 
                return 
            session.close()
        return node_message
    
    def build_neo4j_query_and_values(self):
        odoo_id = self.id 
        odoo_name = self.message['display_name']
        odoo_body = self.message['body']
        odoo_date = self.message['date']
        
        ohp = OdooHTMLParser()
        ohp.feed(odoo_body)
        ohp.close()
        mt = ohp.text

        q = Pypher()
        q.MERGE.node('mt', 'Message', number = odoo_id).SET(
            __.mt.__Name__ == odoo_name,
            __.mt.__Date__ == odoo_date,
            __.mt.__Text__ == mt
        )
        q.WITH.mt
        q.MATCH.node('i', 'Issue').WHERE.i.__Number__ == self.parent.id
        q.MERGE.node('i').rel_out(labels='MESSAGE').node('mt')
        cypher = str(q)
        params = q.bound_params
        #print("Pypher: ", cypher)
        #print("  with: ", params)
        return cypher, params
    
    def skip_me(self):
        odoo_body = self.message['body']
        odoo_subtype = self.message['subtype_id']
        if odoo_subtype == False:
            return False
        type = odoo_subtype[0]
        #    if (type == 78) OR # 'Issue Stage Changed'
        #    (type == 72) OR # 'Issue Blocked'
        #    (type == 71) OR # 'Issue Assigned'
        #    (type == 70): # 'Issue Created'
        if type in {70,71,72,78}:
            return True
        return False 
