#
# MigrationFilter
#
# Generic (parent) 
# Filter and Modifier 
#
# Gert Wijsman
# November 2024

import os

class MigrationFilter:

    def __init__(self):
        filterpath = os.getenv("FILTERFOLDER")
        self.csv_file_path = filterpath 

    def csv_filename(self):
        f = self.csv_file_path + "/" + self.csv_file
        return f
