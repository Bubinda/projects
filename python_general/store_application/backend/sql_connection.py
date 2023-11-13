import datetime
import mysql.connector

__connection = None


def establish_connection():

    global __connection
    if __connection is None:

        __connection = mysql.connector.connect(user='root',
                                            password='-/yHRN=vw2w?',
                                            host='127.0.0.1',
                                            database='grocery_store')

    return __connection


def close_connection():

    global __connection
    if __connection is None:
        pass

    else:
        __connection.close()
