#!/usr/bin/env python3
"""Retrieve all documents with a topic among topics"""


def schools_by_topic(mongo_collection, topic):
    """Return all docs with a topic passed"""
    fetched = mongo_collection.find({'topics': {'$in': [topic]}})
    return [item for item in fetched]
