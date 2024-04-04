"""
File: CollegeSearch.py
Author: Ema Ikeda
Date: 1/20/24
Description: Program that connects to MongoDB database containing college programs. 
Returns query result to be displayed on search results page
"""

"""TODO: 
1. make functions private except test()
3. Verify which parameters to accept as input in search_college()
4. Research if MongoDB queries can be sanitized
5. Determine which column to display in search results screen"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from ConnectToMongoDB import connectToDB

class CollegeDatabaseHandler():
    # constructor
    def __init__(self, database):
        self.database = database
        self.connection = None
        self.cursor = None
        self.client = None

    # todo: make this function private after testing
    def connect_to_db(self):
        self.client = connectToDB()

    # helper function to execute MongoDBs query and returns query result.
    # todo: 
        # 2. make it private 
    def execute_query(self, city):
        collection = self.client[self.database]['Schools']
        testQuery = {"city": city}
        results = list(collection.find(testQuery))
        return results

    # Disconnect from database
    # todo: 
        # 2. make private
    def disconnect_db(self):
        if(self.client):
            self.client.close()

    """Search algorithm that connects to MongoDB database, 
    executes MongoDB query based on string query, then returns query result"""
    # todo: 
    def search_college(self, city):
        self.connect_to_db()
        search_results = self.execute_query(city)
        self.disconnect_db()
        return search_results # display this using another function

# Debugging function
def test():
    search = CollegeDatabaseHandler("Schools") # todo: check which database to use
    results = search.search_college("Seattle")
    for program in results:
        print(program)

test()