#
# OdooIssues
#
# wrapper with functionality specific for the issue list
# implemented an iter over the list
#
# Gert Wijsman
# August 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging 
from .OdooIssue import OdooIssue 

logger = logging.getLogger(__name__)

class OdooIssues:
    def __init__(self, odoo_info):
        self.odoo_info = odoo_info
        self.list_of_issueids = []
        self.list_of_issues = []
        self.get_list()
        logger.debug(self.__str__())

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

        
