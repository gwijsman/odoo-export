#
#
class OdooIssue:
    def __init__(self, odoo_info, id):
        # print("Init issue: ", id)
        self.id = id
        self.odoo_info = odoo_info
        self.issue = False
        self.get_from_odoo() 
        
    def __str__(self):
        return f"OdooIssue with id: {self.id}"
        
    def get_from_odoo(self):
        try:
            self.issue = self.odoo_info.kw_read_result('project.issue', [self.id])
        except Error as v:
            print("ERROR AUTHENTICATING", v)
            self.issue = False
        return self.issue
