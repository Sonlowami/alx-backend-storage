#!/usr/bin/env python3
"""Inserts a new document ina  collection"""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection based on kwargs"""
    inserted = mongo_collection.insert_one(kwargs)
    return inserted.inserted_id
