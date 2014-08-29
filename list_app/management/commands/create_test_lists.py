from list_site import settings
from django.core.management.base import BaseCommand, CommandError
import sys, os, shutil, pdb, subprocess

def get_list_by_owner_name(lists, name):
    for list in lists:
        if list.name == name:
            return list
    return None

class List:
    owners = []
    name = None
    
    def __init__(self, name, owners):
        self.name = name
        self.owners = owners

#parse the .txt file containing the lists to be created
#return an array of 'List's
def parse_input_file(file_path):
    input_file = None
    lists = []
    
    try:
        input_file = open(file_path, 'r')
    except OSError as err:
        print err
        return None

    line = input_file.readline().strip('\n')
    while(line):
        list_name = line.split(':')[0]
        list_owners = (line.split(':')[1]).split(',')
        lists.append(List(list_name, list_owners))
         
        line = input_file.readline().strip('\n')
                
    return lists

def create_mailman_input_files(lists, output_directory):
    if not os.path.exists(output_directory):
        print("output_directory does not exist!")
        return False
    
    for list in lists:
        #append all owners in the list structure except for the first one which will be supplied as the first owner
        #when the list is created in mailman
        if os.path.exists(output_directory+'/'+list.name):
            raise Exception('duplicate list')

        mailman_file = open(output_directory + '/' + list.name, 'a')

        #add each owner to the list
        for i in range(1,len(list.owners)):
            mailman_file.write("mlist.owner.append('"+list.owners[i]+"')\n")
        
        mailman_file.close()
         
    return True

def create_mailman_lists(lists, mailman_input_file_dir):
    if not os.path.exists(mailman_input_file_dir):
        print("mailman_input_file_dir does not exist!")
        return False   
        
    #pdb.set_trace() 
    list_files = os.listdir('tmp')
    for file_name in list_files:
        
        list = get_list_by_owner_name(lists, file_name)
        if not list:
            print('owner not found!')
            return False
            
        #pdb.set_trace()

        executable_path = os.path.join(settings.MAILMAN_SCRIPTS_DIR, 'newlist')
        executable_args = ' ' + file_name + ' ' + list.owners[0] + ' ' + 'test123'
        subprocess.call(executable_path + executable_args, shell=True)
        
        script_path = os.path.join(settings.MAILMAN_SCRIPTS_DIR, 'config_list')
        script_args = ' -i ' + '/data/ssg-test/htdocs/list_expiration/tmp/' + file_name + ' ' + file_name
        subprocess.call(script_path + script_args, shell=True)

     
class Command(BaseCommand):

    def handle(self, *args, **options):
        input_file = 'test_lists.txt'
         
        lists = parse_input_file(input_file)
        if not lists:
            return 
        
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        
        #pdb.set_trace()

        if not create_mailman_input_files(lists, 'tmp'):
            print('failed to create mailman input files')
            return 
        
        create_mailman_lists(lists, 'tmp')
        
        #shutil.rmtree('tmp')


