
#
# Neo4jDB
#
# wrapper with functionality specific for the Neo4j database
#
# 
# Gert Wijsman
# October 2024
#
# inspriation:
# I love Object Oriented programming 
#

import logging

from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class Neo4jDB:
    def __init__(self):
        logger.debug("Activate Neo4j Database: %i", 1)
        uri = "neo4j://172.17.2.219:7687"
        user = "neo4j"
        passwd = "gertgert"
        self.driver = GraphDatabase.driver(uri, auth=(user, passwd))
        self.verify()

    def session(self):
        return self.driver.session()

    def verify(self):
        try:
            info = self.driver.get_server_info()
            print(info)
        except:
            logger.error("Database configuration wrong!")
            self.close() 
            exit(1)
        
    def close(self):
        self.driver.close() 
