#
# OdooInfo
#
# wrapper with functionality specific for the database connection
# configuration is done via .env (see sample and do-export.py 
# 
# Gert Wijsman
# August 2024
#
# inspriation:
# I love Object Oriented programming 
#

from xmlrpc.client import ServerProxy, Error
import logging

logger = logging.getLogger(__name__)

class OdooInfo:
    def __init__(self, db, username, password, host, debug_limit=None):
        self.db = db
        self.username = username 
        self.password = password
        self.host = host
        self.url = "https://" + host + "/xmlrpc/2/"
        self.uid = False
        self.odoo_version = False 
        self.authenticate()
        self.debug_limit = debug_limit
        logger.info("Initialized Odoo Connection")
        logger.debug('Connected to: %s', self.url)

    def __str__(self):
        return f"{self.host} ; {self.db} ; {self.odoo_version} ; {self.uid} ; {self.username}"

    def authenticate(self):
        with ServerProxy(self.url + "common") as proxy:
            try:
                self.odoo_version = proxy.version()['server_version']
                logger.info("Running version of ODOO: %s", self.odoo_version)
            except Exception as v:
                logger.critical("ERROR connecting to DB: %s", v)

            try: 
                self.uid = proxy.authenticate(self.db, self.username, self.password, {})
            except Exception as v:
                logger.critical("ERROR AUTHENTICATING %s", v)
                
            if (self.uid != False): 
                logger.info('Authenticated as user id: %s', self.uid)
            else: 
                logger.critical('Authentication wrong, please correct!')
                exit(1)

    def kw_search_result(self, model, domain):
        with ServerProxy(self.url + 'object') as models:
            if self.debug_limit == None:
                result_list = models.execute_kw(self.db, self.uid, self.password,
                                                model, 'search', domain, {'offset': 0})
            else:
                result_list = models.execute_kw(self.db, self.uid, self.password,
                                                model, 'search', domain, {'offset': 0, 'limit': self.debug_limit})
                logger.warning("CURRENTLY LIMITED TO %i RECORDS!", self.debug_limit)
        return result_list 
        
    def kw_read_result(self, model, domain):
        with ServerProxy(self.url + 'object') as models: 
            result_list = models.execute_kw(self.db, self.uid, self.password,
                                            model, 'read', domain)
            #, {'offset': 0, 'limit': 5})
        return result_list 
        
    def kw_check_access_result(self, model, domain):
        with ServerProxy(self.url + 'object') as models: 
            result = models.execute_kw(self.db, self.uid, self.password,
                                       model, 'check_access_rights', domain,
                                       {'raise_exception': False})
        return result

    def kw_create(self, model, domain):
        with ServerProxy(self.url + 'object') as models: 
            result_list = models.execute_kw(self.db, self.uid, self.password,
                                            model, 'create', domain)
        return result_list 
        
