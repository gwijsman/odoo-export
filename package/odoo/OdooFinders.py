#
# OdooFinders
#
# This class should not be intantiated 
#
# Gert Wijsman
# December 2024
#

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
        from .OdooPartnerFinder import OdooPartnerFinder
        from .OdooCustomerFinder import OdooCustomerFinder
        from .OdooContactFinder import OdooContactFinder
        from .OdooCountryFinder import OdooCountryFinder
        from .OdooStateFinder import OdooStateFinder
        from .OdooCategoryFinder import OdooCategoryFinder
        from .OdooTitleFinder import OdooTitleFinder
        from .OdooCurrencyFinder import OdooCurrencyFinder # todo
        from .OdooProductFinder import OdooProductFinder
        from .OdooTaxFinder import OdooTaxFinder
        from .OdooUomFinder import OdooUomFinder
        # place the finder imports here to prevent circular imports 
        f = OdooCountryFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooStateFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooCategoryFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooTitleFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        fcu = OdooCustomerFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(fcu)
        fco = OdooContactFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(fco)
        f = OdooPartnerFinder(odoo_in_info, odoo_out_info)
        f.set_related_finders(fcu, fco)
        OdooFinders.add_finder(f)
        f = OdooCurrencyFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooProductFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooUomFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)
        f = OdooTaxFinder(odoo_in_info, odoo_out_info)
        OdooFinders.add_finder(f)

        
        
