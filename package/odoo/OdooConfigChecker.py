#
# OdooConfigChecker
#
# Gert Wijsman
# Januari 2025
#

import logging

logger = logging.getLogger(__name__)

class OdooConfigChecker():

    def __init__(self, odoo_info):
        self.odoo_info = odoo_info

    def get_config_settings(self):
        domain = [[['name', 'ilike', '*']]]
        domain = [[]]
        print(self.odoo_info)
        settings = self.odoo_info.kw_search_result('ir.config_parameter', domain)
        print(settings)
        if len(settings) == 0:
            logger.warning("No settings found for %s", '*')
            return False 
        elif len(settings) > 1:
            logger.warning("More settings found for %s", '*')
        nid = settings[0]
        for i in settings:
            domain = [[i]]
            print(domain)
            # result = odoo_info.kw_delete('config.settings', domain)
            # result = odoo_info.kw_read_result('product.template', [self.id])
            result = self.odoo_info.kw_read_result('ir.config_parameter', domain)
            print(result)

    #res.config.settings
    #group_product_variant

    def check(self):
        # self.get_config_settings() 
        logger.debug("Check the odoo config")
