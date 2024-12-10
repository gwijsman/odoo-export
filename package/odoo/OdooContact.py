#
# OdooContact
#
# wrapper with functionality specific for the contact itself
#
# 
# Gert Wijsman
# November 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging
#from .OdooHTMLParser import OdooHTMLParser
#from .OdooAttachments import OdooAttachments
#from .OdooAttachment import OdooAttachment
#from ..neo4j.Neo4jDB import Neo4jDB
#from pypher import Pypher, __
from .OdooPartner import OdooPartner
from .OdooCustomer import OdooCustomer 

logger = logging.getLogger(__name__)

class OdooContact(OdooPartner):
    def __init__(self, odoo_info, id):
        logger.debug("Init Contact: %i", id)
        super().__init__(odoo_info, id)

    def external_name(self):
        return "Contact" 
        
    def write_to_database_keys(self):
        return [
            'name',
            'email',  
            'active',
            'is_company',
            'street',
            'street2',
#            'street3',
#            'state', 
            'zip',
            'city', 
            'website',
            
#            'supplier', 
#            'company_id',
            'parent_id'
#            'country_id'
        ]

    def get_company(self, parent_id):
        return OdooCustomer(self.odoo_info, parent_id) 

    def get_join_info(self, odoo_out_info):
        self.company = self.get_company(self.data()['parent_id'][0])
        name = self.company.data()['name'] 
        target_id = OdooCustomer.get_target_id(odoo_out_info, 'name', name)
        self.data()['parent_id'] = target_id 
