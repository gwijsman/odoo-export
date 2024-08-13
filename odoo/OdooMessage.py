#
#

from .OdooHTMLParser import OdooHTMLParser

class OdooMessage:
    def __init__(self, parent, id):
        self.id = id
        self.parent = parent 
        self.odoo_info = parent.odoo_info
        self.message = self.get_from_odoo()
        self.folder = parent.folder
        # self.debug_dump(False)
        # self.debug_dump()
        
    def __str__(self):
        if self.message != False:
            title = self.message['display_name']
        else:
            title = "empty/no-access"
        return f"OdooMessage with id: {self.id} - {title}"
        
    def get_from_odoo(self):
        try:
            return self.odoo_info.kw_read_result('mail.message', [self.id])
        except Error as v:
            print("ERROR AUTHENTICATING", v)
            return False

    def debug_dump(self, with_keys=True):
        if self.message == False:
            print(self)
            return
        if with_keys:
            print("==========", self.id)
            print(self)
            print("==========", self.id)
            for i_key in self.message.keys():
                print(i_key, ": ", self.message[i_key])
        else:
            print("==========", self.id)
            print(self)
            print("==========", self.id)
            for i_key in [
                    'display_name',
                    'body',
                    'create_date', 
                    'create_uid']: 
                print(i_key, ": ", self.message[i_key])
        print("==========", self.id)
        
    def write_to_text_file(self, folder):
        # folder is the folder to write the file to
        # subfoder div 100?!? (only if needed)
        self.folder = folder
        filename = self.folder + '/' + str(self.id) + '.txt'
        try:
            f = open(filename, 'w') # replace with 'x' later (when no overwriting needed!) 
        except:
            print("Failed opening file: ", filename)
            return 
        # try: 
        self.write_info(f)
        # except:
        # print("wrong")
        f.close() 
        print("created file: ", filename)

    def write_info(self, f):
        i = self.issue
        if i == False:
            f.write("no access to issue")
            return
        for i_key in [
                'id', 
                'display_name',
                'product',  
                'name',
                'description',
                'message_summary',
                'partner_id',
                'analytic_account_id',
                'user_id',
                'priority',
                'issue_stage_id',
                'email_from',
                'message_ids']:
            f.write(i_key)
            f.write(": ")
            f.write(str(self.issue[i_key]))
            f.write('\n')
        self.write_description(f)
        self.write_messages(f)

    def write_body(self, f):
        b = self.message['body']
        f.write('\n')
        f.write('\n')
        f.write('Body: ') 
        f.write('\n')
        
        ohp = OdooHTMLParser()
        ohp.feed(b)
        ohp.close()
        f.write(ohp.text)
        f.write('\n')
        f.write('\n')

    def write_on(self, f):
        f.write(self.__str__())
        f.write('\n')
        self.write_body(f)
        f.write('\n')
