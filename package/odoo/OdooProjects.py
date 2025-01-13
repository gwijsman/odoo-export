#
# OdooProjects
#
# wrapper with functionality for the project list
# implemented an iter over the list
#
# domain could be: [[['is_company', '=', True]]]
#
# Gert Wijsman
# Januari 2025
#
# inspriation:
# I love Object Oriented programming 
#

import logging 
from .OdooProject import OdooProject

logger = logging.getLogger(__name__)

class OdooProjects:

    def __init__(self, odoo_info, domain=[[]]):
        self.odoo_info = odoo_info
        self.domain = domain 
        self.list_of_projectids = []
        self.list_of_projects = []
        self.get_list_ids()
        self.get_list_details()
        logger.debug(self.__str__())

    def __str__(self):
        return f"OdooProjects: List of {len(self.projects())} projects"

    def projects(self):
        return self.list_of_projects 

    def projectids(self):
        return self.list_of_projectids 

    def __iter__(self):
        self.index = 0
        return self 

    def __next__(self):
        if self.index < len(self.projects()):
            x = self.index 
            self.index += 1
            item = self.projects()[x] 
            return item 
        else: 
            raise StopIteration
    
    def get_list_ids(self):
        self.list_of_projectids = self.odoo_info.kw_search_result('project.project', self.domain)

    def get_list_details(self):
        for id in self.projectids():
            self.projects().append(OdooProject(self.odoo_info, id))

    def first(self):
        if len(self.projects()) == 0:
            return False
        else:
            return self.projects()[0]

