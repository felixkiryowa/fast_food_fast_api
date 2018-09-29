"""
This module handles the database set up
"""
import psycopg2

def database_connection():
    """
    This method creates a connection to the databse
    "dbname='stackoverflow' user='celestemiriams' host='localhost' password='lutwama@2' port='5432'"
    :retun: connection
    """

    conn = psycopg2.connect(
        host="localhost", database="Fast_food_fast", user="francis", password="atagenda1@"
    )
    return conn