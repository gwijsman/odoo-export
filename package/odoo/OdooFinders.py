#
# OdooFinders
#
# This class should not be intantiated 
#
# Gert Wijsman
# December 2024
#

from .OdooFinder import OdooFinder
from .OdooCountryFinder import OdooCountryFinder
from .OdooStateFinder import OdooStateFinder
from .OdooCategoryFinder import OdooCategoryFinder
from .OdooTitleFinder import OdooTitleFinder

class OdooFinders():

    finders = {}

    def add_finder(f):
        OdooFinders.finders[f.key] = f

    def get_finder(k):
        return OdooFinders.finders[k]
    
    def show_finders():
        fs = OdooFinders.finders
        for k in fs.keys():
            f = fs[k] 
            print(k, ":  ", f.name, " (", type(f).__name__, ")")

    def initialize(odoo_in_info, odoo_out_info):
        f = OdooCountryFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooStateFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooCategoryFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooTitleFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)

        
        
