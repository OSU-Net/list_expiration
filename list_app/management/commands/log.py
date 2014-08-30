from django.core.management.base import BaseCommand, CommandError
import os, errno, stat, os.path

import pdb

BUFFER_SIZE = 256
FIFO_DIR = 'tmp'
FIFO_NAME = 'server_log_FIFO'

class Command(BaseCommand):
        
    def handle(self, *args, **options):

        if not os.path.exists(FIFO_DIR+"/"+FIFO_NAME):
            os.makedirs(FIFO_DIR)
            os.mkfifo(FIFO_DIR+'/'+FIFO_NAME)
            
        io = os.open(FIFO_DIR+'/'+FIFO_NAME, os.O_RDONLY | os.O_NONBLOCK)
        print "Logger listening..."        
        
        while True:
            #check for a message from the server log and output it if necessary
            try:
                buff = os.read(io, BUFFER_SIZE) 
            except OSError as err:
                if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                    buff = None
                else:
                    raise Exception("Issue reading FIFO file")
            if buff:
                print buff
