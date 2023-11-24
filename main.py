import logging
import os
import socket
from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from web import routes
import threading

import requests
from requests import get
from dbmgr import db

CORS(routes.app)

dbfilename = "envplatdata.db"

# set up the logger
#logging.basicConfig(filename="envplatnav.log", format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)

def main():
    logging.info("***************************************************************")
    logging.info("EnvDataPlatform Data Collector has started")
    logging.info("Running %s", __file__)
    logging.info("Working directory is %s", os.getcwd())
    logging.info("SQLITE Database file is %s", dbfilename)

    localipaddress = "IP: Unknown"
    try:
        hostname = socket.gethostname()
        externalip = get('https://api.ipify.org').text
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        localipaddress = s.getsockname()[0]
        logging.info("Hostname is %s", hostname)
        logging.info("Local IP is %s and external IP is %s", localipaddress, externalip)

    except Exception as e:
        logging.exception("Exception occurred")
        logging.error("Unable to get network information")


datacollectors = ["192.168.1.206", "192.168.1.240"]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

    # create connection to our database
    mydb = db.createConnection(dbfilename)

    if mydb is not None:
        # create table
        db.createTable(mydb)
        mydb.commit()

        # log start up message
        logging.info("***************************************************************")
        logging.info("Data Access Server has started")
        logging.info("Running %s", __file__)
        logging.info("Working directory is %s", os.getcwd())

        try:
            hostname = socket.gethostname()
            OurHostname = hostname
            externalip = requests.get('https://api.ipify.org').text
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
            localipaddress = s.getsockname()[0]
            logging.info("Hostname is %s", hostname)
            logging.info("Local IP is %s and external IP is %s", localipaddress, externalip)

        except Exception as e:
            logging.error("Unable to get network information")

        # start the data collection
        datacollectorthread = threading.Thread(target = db.collector, daemon = False, args=(datacollectors, dbfilename))
        datacollectorthread.start()

        logging.getLogger('werkzeug').level = logging.ERROR
        logging.info('Starting web server on port 8080...')
        routes.app.run(debug=True, host='0.0.0.0', port = 8080)

    else:
        logging.error("Unable to create or access SqlLite3 database")



