from list_site import settings
from django.core.management.base import BaseCommand, CommandError
import sys, os, shutil, pdb, subprocess

class List:
    owners = []
    name = None

def get_list_by_owner_name(lists, name):
    for list in lists:
        if list.name == name:
            return list
    return None

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

    line = input_file.readline()
    while(line):
        list = List()
        list.name = line.split(':')[0]
        list_owners = line.split(':')[1]
        for owner_name in list_owners:
            list.owners.append(owner_name)

        line = input_file.readline()

def create_mailman_input_files(lists, output_directory):
    if not os.path.exists(output_directory):
        print("output_directory does not exist!")
        return False
    
    for list in lists:
        #append all owners in the list structure except for the first one which will be supplied as the first owner
        #when the list is created in mailman
        if os.path.exists(mailman_file_name):
            raise Exception('duplicate list')
        
        mailman_file = open(output_directory + '/' + list.name, 'a')

        #add each owner to the list
        for i in range(1,len(list.names)):
            mailman_file.write("mlist.owner.append('"+list.names[i]+"')\n")
    
    return True

def create_mailman_lists(lists, mailman_input_file_dir):
    if not os.path.exists(mailman_input_file_dir):
        print("mailman_input_file_dir does not exist!")
        return False   
    
        list_files = os.listdir('tmp')
        for file_name in list_files:
            first_owner = get_list_by_owner(lists, file_name)
            if not first_owner:
                raise Exception('list owner not found!')

     
class Command(BaseCommand):

    def handle(self, *args, **options):
        input_file = 'test_lists.txt'
        
        lists = parse_input_file(input_file)
        if not lists:
            return 
        
        if not create_mailman_input_files(lists, 'tmp'):
            print('failed to create mailman input files')
            return 
        
                    
