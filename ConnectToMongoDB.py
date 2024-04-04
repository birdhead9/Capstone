"""
File: ConnectToMongoDB.py
Author: Ema Ikeda
Date: 1/10/24
Description: Program that connects to MongoDB database
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# todo: modify this function to allow program to connect to different database
def connectToDB():
    # Note: Make sure your IP Address is whitelisted!
    uri = "mongodb+srv://ema123:ema123@schools.rswmjwr.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client