import datetime
import mysql.connector

__connection = None


def establish_connection():

    global __connection
    if __connection is None:

        db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=5,
            host='127.0.0.1',
            database='grocery_store',
            user='root',
            password='-/yHRN=vw2w?'
        )

        __connection = db_pool.get_connection()

        # __connection = mysql.connector.connect(user='root',
        #                                     password='-/yHRN=vw2w?',
        #                                     host='127.0.0.1',
        #                                     database='grocery_store')

    return __connection


def close_connection():

    global __connection
    if __connection is None:
        pass

    else:
        __connection.close()
