from django.core.management.base import BaseCommand, CommandError
import sys

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
        while True:
            line = file.readline()
            if not line:
                break
            
            line_strs = line.split(':')
            list_name = line_strs[0]      
            list_owners_strs = line_strs[1].split(',')    
            
            #create the list

            #add each owner to the list
        
        #create mailman lists


