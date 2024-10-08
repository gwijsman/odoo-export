#
# OdooAttachments
#
# wrapper with functionality specific for an Attachment list from Odoo 
#
# Main purpose is dumping the Attachments (binary) to file
# The LLM should be able to refernce the attachment from the txt file
# this is just for reference 
# 
# Gert Wijsman
# August 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging
from .OdooAttachment import OdooAttachment

logger = logging.getLogger(__name__)

class OdooAttachments:
    def __init__(self, odoo_info, parent):
        logger.debug("Init Attachments for: %i", parent.id)
        self.id = parent.id
        self.odoo_info = odoo_info
        self.parent = parent
        self.attachments = self.get_from_odoo()
        self.folder = self.parent.folder 
        
    def __str__(self):
        if self.attachments != False:
            s = str(len(self.attachments))
        else:
            s = "empty/no-access"
        return f"OdooAttachment list size: {s}"

    def __iter__(self):
        self.index = 0
        return self 

    def __next__(self):
        if self.index < len(self.attachments):
            x = self.index 
            self.index += 1
            item = self.attachments[x] 
            return item 
        else: 
            raise StopIteration

    def get_from_odoo(self):
        try:
            d = self.parent.domain_for_attachments() 
            l = self.odoo_info.kw_search_result('ir.attachment', d)
            return l 
        except Exception as v:
            logger.error("ERROR AUTHENTICATING %s", v)
            return False
