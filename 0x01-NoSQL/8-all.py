#!/usr/bin/env python3
"""Display all the documents in a collection."""


def list_all(mongo_collection):
    """List all the documents in a collection."""
    return list(mongo_collection.find())
