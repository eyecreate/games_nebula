import os
import sys

def set_nebula_dir():
    
    if os.getenv('NEBULA_DIR') == None:
        nebula_dir = sys.path[0]
    else:
        nebula_dir = os.getenv('NEBULA_DIR')
        
    return nebula_dir
