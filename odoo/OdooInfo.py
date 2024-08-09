#
#
from xmlrpc.client import ServerProxy, Error

class OdooInfo:
    def __init__(self, db, username, password, host):
        self.db = db
        self.username = username 
        self.password = password
        self.host = host
        self.url = "https://" + host + "/xmlrpc/2/"
        self.uid = False
        self.odoo_version = False 
        self.authenticate()

    def __str__(self):
        return f"{self.host} ; {self.db} ; {self.odoo_version} ; {self.uid} ; {self.username}"

    def authenticate(self):
        with ServerProxy(self.url + "common") as proxy:
            try:
                self.odoo_version = proxy.version()['server_version']
                print("Running version of ODOO: ", self.odoo_version)
            except Error as v:
                print("ERROR", v)

            try: 
                self.uid = proxy.authenticate(self.db, self.username, self.password, {})
            except Error as v:
                print("ERROR AUTHENTICATING", v)
                
            if (self.uid != False): 
                print('Authenticated as user id: ', self.uid)
            else: 
                print('Authentication wrong, please correct!')
                #exit()
                os._exit(1)

    def kw_search_result(self, model, domain):
        with ServerProxy(self.url + 'object') as models: 
            result_list = models.execute_kw(self.db, self.uid, self.password,
                                            model, 'search', domain, {'offset': 0, 'limit': 5})
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
