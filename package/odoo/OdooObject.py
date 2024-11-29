#
# OdooObject
#
# all Odoo object inherit from me
#
# Gert Wijsman
# Nov 2024
#
class OdooObject:

    def __init__(self, odoo_info, id):
        self.id = id
        self.odoo_info = odoo_info

    def data(self):
        # override in sub class with data field 
        return False

    def external_name(self):
        # override with user friendly name 
        return "OdooObject"

    def __str__(self):
        if self.data() != False:
            title = self.data()['display_name']
        else:
            title = "empty/no-access"
        return f"{self.external_name()} with id: {self.id} - {title}"

    def is_valid(self):
        return self.data() != False
    
    def debug_dump(self, with_keys=True):
        if self.data() == False:
            print(self)
            return
        print("==========Start Dump: ", self.id)
        print(self)
        print("==========", self.id)
        for i_key in self.keys_to_dump():
            print(i_key, ": ", self.data()[i_key])
        print("==========End Dump:", self.id)

    def debug_dump_keys(self):
        if self.data() == False:
            print(self)
            return
        print("==========", self.id)
        for i_key in self.data().keys():
            print(i_key.strip())
        print("==========", self.id)
        print(self)

    def keys_to_dump(self):
        return self.alfa_keys() + self.one_join_keys() + self.multi_join_keys() 
    
    def alfa_keys(self):
        return [
            'id',
            'name', 
            'display_name',
            'active'
        ]

    def boolean_field_keys(self):
        return [
            'active',
        ]
    def one_join_keys(self):
        return [
            'parent_id'
        ]

    def multi_join_keys(self):
        return [
            'child_ids'
        ]

    def write_to_database_keys(self):
        return [
            'name',
            'active',
            'parent_id'
        ]

    def compile_field_list(self):
        field_list = {}
        for i_key in self.write_to_database_keys():
            value = self.data()[i_key]
            if (value == False) and not(i_key in self.boolean_field_keys()):
                continue 
            else:
                field_list[i_key] = value 
        return field_list 
    
