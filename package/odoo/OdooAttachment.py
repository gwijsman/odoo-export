#
# OdooAttachment
#
# wrapper with functionality specific for the Attachment from Odoo
#
# Main purpose is dumping the Attachment (binary) to file
# The LLM should be able to refernce the attachment from the txt file
# this is just for reference 
# 
# Gert Wijsman
# August 2024
#
# inspriation:
# I love Object Oriented programming 
#

import os
import logging
import base64
from pypher import Pypher, __

logger = logging.getLogger(__name__)

class OdooAttachment:
    def __init__(self, odoo_info, parent, id):
        self.id = id
        self.odoo_info = odoo_info
        self.parent = parent
        self.attachment = False 
        self.attachment = self.get_from_odoo_by_id()
        self.folder = self.parent.folder 
        logger.debug("Initialized Attachment: %s", self.__str__())
        
    def __str__(self):
        if self.is_valid():
            title = self.attachment['name']
        else:
            title = "Empty/No Access"
        return f"OdooAttachment with id: {self.parent.id} - {self.id} - {title}"

    def is_valid(self):
        return self.attachment != False 
        
    def get_from_odoo_by_id(self):
        try:
            l = self.odoo_info.kw_read_result('ir.attachment', [self.id])
            if len(l) != 1:
                logger.error("Unexpected result in number of attachments, should be one for %s", self.__str__())
                return False
            else:
                return l[0] 
        except Exception  as v:
            logger.error("ERROR %s", v)
            return False

    def full_filename(self):
        if self.folder != False:
            folder = self.folder
        else:
            folder = ""
        return folder + '/attachments/' + str(self.parent.id) + '-' + str(self.id) + '-' + self.attachment['name'] 

    def full_url(self):
        urloutputfolder = os.getenv('URL_OUTPUT_FOLDER')
        return urloutputfolder + '/attachments/' + str(self.parent.id) + '-' + str(self.id) + '-' + self.attachment['name'] 
        
    def save(self):
        if self.attachment == False:
            return 
        filename = self.full_filename()
        logger.debug("SAVE: %s", filename) 
        with open(filename, 'wb') as f:
            downloaded_file = base64.b64decode(self.attachment['datas'])
            f.write(downloaded_file)

    def add_url(self, f):
        f.write('\n')
        f.write('file: ')
        f.write(self.full_filename())
        f.write('\n')
        f.write('url: ')
        f.write(self.full_url())
        f.write('\n')
        
    def join_to_issue(self, neo4jdb):
        if not self.is_valid():
            logger.warning("Attachment invalid! (%i)", self.id)
            return False 
        logger.info("Create Attachment Reference in neo4j for issue %i", self.parent.id)
        query, values = self.build_neo4j_query_and_values()
        with neo4jdb.session() as session:
            try:
                result = session.run(query, values)
                node_attachment = result.single()
            except Exception as v:
                logger.error("ERROR %s", v)
                session.close() 
                return 
            session.close()
        return node_attachment
    
    def build_neo4j_query_and_values(self):
        odoo_id = self.id 
        fn = self.full_filename()
        fu = self.full_url()
        
        q = Pypher()
        q.MERGE.node('at', 'Atachment', number = odoo_id).SET(
            __.at.__Fileame__ == fn,
            __.at.__URL__ == fu
        )
        q.WITH.at
        q.MATCH.node('i', 'Issue').WHERE.i.__Number__ == self.parent.id
        q.MERGE.node('i').rel_out(labels='ATTACHMENT').node('at')
        cypher = str(q)
        params = q.bound_params
        #print("Pypher: ", cypher)
        #print("  with: ", params)
        return cypher, params 
