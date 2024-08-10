#
#
class OdooIssue:
    def __init__(self, odoo_info, id):
        # print("Init issue: ", id)
        self.id = id
        self.odoo_info = odoo_info
        self.issue = self.get_from_odoo()
        
    def __str__(self):
        if self.issue != False:
            title = self.issue['display_name']
        else:
            title = "empty/no-access"
        return f"OdooIssue with id: {self.id} - {title}"
        
    def get_from_odoo(self):
        try:
            return self.odoo_info.kw_read_result('project.issue', [self.id])
        except Error as v:
            print("ERROR AUTHENTICATING", v)
            return False

