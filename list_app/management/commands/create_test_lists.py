from list_site import settings
from django.core.management.base import BaseCommand, CommandError
import sys, os, shutil, pdb, subprocess

class Command(BaseCommand):        

    #call mailman utilities to create a list and add it's owners specified in the tmp/{list_name} file
    def mailman_create_list(self, list_name, first_owner):
    #call mailman utility to create lists inside of mailman
    #./newlist ph_211 wasingej@onid.oregonstate.edu test123

        #open the file containing list owners in tmp/{list_name}
        try:
            file = open('tmp/'+list_name, 'r')
        except IOError as err:
            print err
            return 

        executable_path = os.path.join(settings.MAILMAN_SCRIPTS_DIR, 'newlist')
        executable_args = list_name + ' ' + first_owner + ' ' + 'test123'
    
        subprocess.call(executable_path + ' ' + executable_args, shell=True)
        
        script_path = os.path.join(settings.MAILMAN_SCRIPTS_DIR, 'config_list')
        script_args = ' -i ' + '/data/ssg-test/htdocs/list_expiration/tmp/' + list_name + ' ' + list_name
        
        try:
            subprocess.call(script_path + script_args)
        except OSError as error:
            pdb.set_trace()
            print error

    def handle(self, *args, **options):
        
        lists_file_name = 'test_lists.txt'

        #open input file
        lists_file = None

        try:
            lists_file = open(lists_file_name, 'r')
        except IOError:
            print('file {0} not found'.format(lists_file))
            return 
                        
        parse_state = 'default'
            
        #parse lists from the input file

        #input file format:
        # list_name1:list_owner1,list_owner2,list_owner3,...
        # list_name2:list_owner,...
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
         
        while True:
            line = lists_file.readline().strip()
            if not line:
                break
            
            line_strs = line.split(':')
            list_name = line_strs[0]      
            list_owners_strs = line_strs[1].split(',')    
            
            #call mailman utility to create the list
            
            mailman_file_name = 'tmp/'+list_name
            #create file to pass to mailman to add owners to the list
            if os.path.exists(mailman_file_name):
                raise Exception('duplicate list')
            
            mailman_file = open(mailman_file_name, 'a')

            #add each owner to the list
            for owner in list_owners_strs:
                mailman_file.write("mlist.owner.append('"+owner+"')\n")
        
         
        lists = os.listdir('tmp')

        for list in lists:
            #open the file and find the name of the first owner
            file = open('tmp/'+list, 'r')

            first_line = file.readline()
            owner = first_line.split("'")[1]
            self.mailman_create_list(list, owner)
            
        #delete temporary files
        shutil.rmtree('tmp')

