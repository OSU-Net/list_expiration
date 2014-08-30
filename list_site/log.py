from multiprocessing import Process, Pipe
import os, errno, stat
import shutil

from async_test.settings import BASE_DIR

import pdb

FIFO_DIR = 'tmp'
FIFO_NAME = 'server_log_FIFO'

def log_str(msg):
    if not os.path.exists(os.path.join(BASE_DIR,FIFO_DIR)):
        os.makedirs(os.path.join(BASE_DIR,FIFO_DIR))
    
    #see if the FIFO exists, if not create it
    if not os.path.exists(os.path.join(BASE_DIR,FIFO_DIR,FIFO_NAME)):
        os.mkfifo(os.path.join(BASE_DIR, FIFO_DIR, FIFO_NAME))

    try:
        fd = os.open(os.path.join(BASE_DIR,FIFO_DIR,FIFO_NAME), os.O_WRONLY | os.O_NONBLOCK)
    except OSError:
        return False

    os.write(fd, msg)

    return True
