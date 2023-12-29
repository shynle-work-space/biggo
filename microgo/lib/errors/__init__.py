"""
# Error centralization 

This module contains code error customization and known error produce by modules,
that will be captured and handled in the code.

Other error not explicitly stated in this module will be treated as outlier, and DEBUG log
"""
from errors.errors import Error
from sqlalchemy.exc import DatabaseError
from pymongo.errors import ConnectionFailure