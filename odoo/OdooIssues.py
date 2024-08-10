#
#

from .OdooIssue import OdooIssue 

class OdooIssues:
    def __init__(self, odoo_info):
        self.odoo_info = odoo_info
        self.list_of_issueids = []
        self.list_of_issues = []
        self.get_list()

    def __str__(self):
        return f"OdooIssues: List of {len(self.list_of_issues)} issues"

    def __iter__(self):
        self.index = 0
        return self 

    def __next__(self):
        if self.index < len(self.list_of_issues):
            x = self.index 
            self.index += 1
            item = self.list_of_issues[x] 
            return item 
        else: 
            raise StopIteration
    
    def get_list(self):
        self.list_of_issueids = self.odoo_info.kw_search_result('project.issue', [[]])
        for id in self.list_of_issueids:
            self.list_of_issues.append(OdooIssue(self.odoo_info, id))

    def issues(self):
        return self.list_of_issues 

