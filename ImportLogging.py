#
# ImportLogging
#
# Setup logging to output and log file on nessary level of information
# 
#
# Gert Wijsman
# August 2024
#
# inspriation:
# I love Object Oriented programming 
#

#

import logging
import sys
import os
        
def setup_logging():
    # configure the root logging
    log = logging.getLogger('root') 

    log.setLevel(logging.DEBUG)
    
    # Console
    # create console handler and set level to debug
    ch1 = logging.StreamHandler(sys.stdout)
    ch1.setLevel(logging.DEBUG)
    formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch1.setFormatter(formatter1)
    log.addHandler(ch1)
    
    # create file handler and set level to debug
    filename = os.getenv('LOG_FILE')
    ch2 = logging.FileHandler(filename)
    ch2.setLevel(logging.INFO)
    formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch2.setFormatter(formatter2)
    log.addHandler(ch2)
