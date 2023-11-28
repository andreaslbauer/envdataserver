import logging
import sqlite3
import requests
import time

# create connection to our dbmgr
def createConnection(dbFileName):
    """ create a database connection to a SQLite database """
    try:
        db = sqlite3.connect(dbFileName)
        logging.info("Connected to database %s which is version %s",
                     dbFileName, sqlite3.version)
        return db

    except Exception as e:
        logging.error(f'Unable to create database {dbFileName}: {e}')

    return None

# create database table
def createTable(mydb):
    createTableSQL = """CREATE TABLE IF NOT EXISTS datapoints (
                                            id integer UNIQUE,
                                            source_ip,
                                            date text,
                                            time text,
                                            datetime text,
                                            temp1 real,
                                            temp2 real,
                                            temp3 real,
                                            temp4 real,
                                            moisture real,
                                            humidity real,
                                            pressure real,
                                            light real,
                                            PRIMARY KEY(source_ip, datetime)
                                        ); """
    try:
        cursor = mydb.cursor()
        cursor.execute(createTableSQL)
        logging.info("Created table %s", createTableSQL)

    except Exception as e:
        logging.error(f'Unable to create table {createTableSQL}: {e}')

# get number of rows in table
def countRows(mydb):
    sql = '''select count(*) from datapoints'''
    try:
        cursor = mydb.cursor()
        result = cursor.execute(sql).fetchone()
        return result[0]

    except Exception as e:
        logging.exception("Exception occurred")
        logging.error("Unable to get row count of table datapoints")

        return 0


def checkForRow(mydb, hostname, datetime):
    sql = '''select count(*) from datapoints where source_ip = ? and datetime = ?'''
    try:
        cursor = mydb.cursor()
        result = cursor.execute(sql, (hostname, datetime)).fetchone()
        return result[0]

    except Exception as e:
        logging.exception("Exception occurred")
        logging.error("Unable to get row count of table datapoints")

        return 0

# insert a record
def insertRow(mydb, row):
    """
    Create a new project into the projects table
    :param mydb:
    :param row:
    :return: newid
    """
    sql = '''INSERT INTO datapoints(id, source_ip, date, time, datetime, temp1, temp2, temp3, temp4, moisture, humidity, pressure, light)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''

    try:
        cursor = mydb.cursor()
        cursor.execute(sql, row)
        logging.debug("Insert %s", row)
        return True

    except Exception as e:
        logging.error(f'Unable to insert row {sql} {row}: {e}')

    return False

def getData(mydb):
    sql = '''select * from datapoints '''
    try:
        cursor = mydb.cursor()
        result = cursor.execute(sql).fetchall()
        return result

    except Exception as e:
        logging.exception("Exception occurred")
        logging.error("Unable to get data")

        return 0


def collector(datacollectors, dbfilename):
    mydb = createConnection(dbfilename)
    logging.info(f'Data collector thread has started')
    rows_count = countRows(mydb)
    logging.info(f'DB has {rows_count} rows')

    while (True):

        for hostname in datacollectors:
            url = f'http://{hostname}/midtermdata.txt'

            try:
                response = requests.get(url=url)
                data = response.json()
                r = None
                l = len(data)
                for item in data:
                    r = item

                    datetimestr = r['D']
                    datestr = datetimestr.split(' ')[0]
                    timestr = datetimestr.split(' ')[1]
                    temp1 = r['T1']
                    temp2 = r['T2']
                    temp3 = r['T3']
                    temp4 = r['T4']
                    moisture = r['M']
                    humidity = r['H']
                    pressure = r['P']
                    light = r['L']

                    try:

                        if checkForRow(mydb, hostname, datetimestr) == 0:
                            #logging.info(
                            #    f'Read data: Host {hostname} Date {datestr} Time {timestr} Temp1 {temp1} Temp2 {temp2} Temp3 {temp3} Temp4 {temp4} Moisture {moisture} Humidity {humidity} Pressure {pressure} Light {light}')
                            data_row = (rows_count, hostname, datestr, timestr, datetimestr,
                                        temp1, temp2, temp3, temp4, moisture, humidity, pressure, light)
                            if insertRow(mydb, data_row):
                                rows_count += 1
                                logging.info(f'Loaded data from: {hostname}')

                            mydb.commit()

                    except Exception as e:
                        logging.error(f'Unable to insert row : {e}')

            except Exception as e:
                logging.error(f'Unable to get data from {url}: {e}')

        time.sleep(240)