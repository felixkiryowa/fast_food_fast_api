import psycopg2

from config import config

def drop_tables():
    
    """ create tables in the PostgreSQL database"""
    command = (
        """
         DROP TABLE IF EXISTS users,orders,menu CASCADE
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ ==  '__main__':
    drop_tables()