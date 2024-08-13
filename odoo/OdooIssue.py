#
#

from .OdooMessage import OdooMessage 
from .OdooHTMLParser import OdooHTMLParser

class OdooIssue:
    def __init__(self, odoo_info, id):
        # print("Init issue: ", id)
        self.id = id
        self.odoo_info = odoo_info
        self.issue = self.get_from_odoo()
        self.issue['product'] = self.product()
        self.folder = False 
        
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

    def debug_dump(self, with_keys=True):
        if self.issue == False:
            print(self)
            return
        print("==========", self.id)
        if with_keys:
            for i_key in self.issue.keys():
                print(i_key)
        print("==========", self.id)
        print(self)
        print("==========", self.id)
        for i_key in [
                'display_name',
                'product',
                'name', 
                'partner_id',
                'analytic_account_id',
                'user_id',
                'priority',
                'issue_stage_id',
                'email_from',
                'message_ids']:
            print(i_key, ": ", self.issue[i_key])
        print("==========", self.id)
        
    def product(self):
        if self.issue == False:
            return 'Unknow'
        analytic_account = self.issue['analytic_account_id'][1]
        if 'SWEG' in analytic_account:
            return 'SWEG'
        elif 'Diagnostics'in analytic_account:
            return 'Diagnostics'
        elif ('Water Office' in analytic_account) or ('WO'in analytic_account):
            return 'Water Office'
        else:
            return 'Unknown'
        
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

    def write_description(self, f):
        d = self.issue['description']
        f.write('\n')
        f.write('\n')
        f.write('Description: ') 
        f.write('\n')
        
        ohp = OdooHTMLParser()
        ohp.feed(d)
        ohp.close() 
        f.write(ohp.text)
        
        f.write('\n')
        f.write('\n')

    def write_messages(self, f):
        msgids = self.issue['message_ids']
        f.write('Messages: ') 
        f.write('\n')
        for id in msgids:
            msg = OdooMessage(self, id)
            msg.write_on(f)
        f.write('\n')

