#!/usr/bin/env python3
"""List all documents in a collection in a mongo database"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """List all documents in a passed mongo collection"""
    final_lst = []
    fetched = mongo_collection.find()
    [final_lst.append(doc) for doc in fetched]
    return final_lst
