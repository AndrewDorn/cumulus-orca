"""
This module contains helper functions for making the database donnection.
"""
import json
import os

def set_env(private_config_json_file):
    """
    Reads the values for database environment variables from a file
    """
    private_config = None
    with open(private_config_json_file) as private_file:
        private_config = json.load(private_file)

    os.environ["DATABASE_HOST"] = private_config["DATABASE_HOST"]
    os.environ["DATABASE_PORT"] = private_config["DATABASE_PORT"]
    os.environ["DATABASE_NAME"] = private_config["DATABASE_NAME"]
    os.environ["DATABASE_USER"] = private_config["DATABASE_USER"]
    os.environ["DATABASE_PW"] = private_config["DATABASE_PW"]
