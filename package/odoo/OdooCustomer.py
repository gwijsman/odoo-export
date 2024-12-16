#
# OdooCustomer
#
# wrapper with functionality specific for the Customer itself
#
# 
# Gert Wijsman
# November 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging
from .OdooPartner import OdooPartner

logger = logging.getLogger(__name__)

class OdooCustomer(OdooPartner):
    def __init__(self, odoo_info, id):
        logger.debug("Init Customer: %i", id)
        super().__init__(odoo_info, id) 

    def external_name(self):
        return "Customer" 
        
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
            'website'
            
#            'supplier', 
#            'company_id',
#            'parent_id'
#            'country_id'
        ]

    def sqlite_table_name(self):
        return 'customer'

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
