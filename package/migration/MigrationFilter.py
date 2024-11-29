#
# MigrationFilter
#
# Generic (parent) 
# Filter and Modifier 
#
# Gert Wijsman
# November 2024

class MigrationFilter:

    def __init__(self):
        self.csv_file_path = "/home/gert.wijsman/python-odoo/odoo-export/filter"

    def csv_filename(self):
        f = self.csv_file_path + "/" + self.csv_file
        return f
