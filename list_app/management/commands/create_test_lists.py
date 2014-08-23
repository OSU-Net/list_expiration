from django.core.management.base import BaseCommand, CommandError
import sys, os, shutil

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='1', type=str)
         
    def handle(self, *args, **options):
        lists_file = options['file']

        #open input file
        file = None

        try:
            file = open(lists_file, 'r')
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
            line = file.readline()
            if not line:
                break
            
            line_strs = line.split(':')
            list_name = line_strs[0]      
            list_owners_strs = line_strs[1].split(',')    
            
            #call mailman utility to create the list
            
            file_name = 'tmp/'+list_name+'_owners'
            #create file to pass to mailman to add owners to the list
            if os.path.exists(file_name):
                raise Exeption('duplicate list')
            
            file = open(file_name, 'a')

            #add each owner to the list
            for owner in list_owners_strs:
                file.write("mlist.owner.append('"+owner+"')\n")
        
        #call mailman utility to create lists inside of mailman


        #delete temporary files
        #shutil.rmtree('tmp')

