from flask import Flask, request, jsonify, make_response, render_template
import logging
from dbmgr import db


app = Flask(__name__, static_folder = '../static',
            template_folder = '../templates')

@app.route('/', methods=['GET'])
def index():
    logging.info('Handle request for /index.html')
    return render_template('index.html')

@app.route('/all', methods=['GET'])
def all():
    logging.info('Handle request for /all.html')

    # create connection to our database
    dbfilename = "envplatdata.db"
    mydb = db.createConnection(dbfilename)
    data = db.getData(mydb)
    return render_template('all.html', data = data)

@app.route('/api/dates', methods=['GET'])
def api_dates():

    # create connection to our database
    dbfilename = "envplatdata.db"
    mydb = db.createConnection(dbfilename)
    cursor = mydb.cursor()
    sql = '''select distinct date from datapoints order by date desc'''
    result = cursor.execute(sql).fetchall()
    data = []
    for item in result:
        for subitem in item:
            data.append(subitem)

    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin',  '*')
    return (response)

@app.route('/daychart', methods=['GET'])
def daychart():
    logging.info('Handle request for /index.html')

    # create connection to our database
    dbfilename = "envplatdata.db"
    mydb = db.createConnection(dbfilename)
    cursor = mydb.cursor()
    sql = '''select distinct date from datapoints order by date desc'''
    result = cursor.execute(sql).fetchall()
    dates = []
    for item in result:
        for subitem in item:
            dates.append(subitem)

    sql = '''select distinct source_ip from datapoints order by source_ip asc'''
    result = cursor.execute(sql).fetchall()
    source_ips = []
    for item in result:
        for subitem in item:
            source_ips.append(subitem)

    data = []

    source_ip = request.args.get('source_ip')
    if source_ip == None:
        source_ip = source_ips[0]

    date = request.args.get('date')
    if date == None:
        date = ''
    else:
        sql = '''select * from datapoints where date is ? and source_ip is ?'''
        result = cursor.execute(sql, (date, source_ip, )).fetchall()

        labels = ['id', 'source_ip' , 'date', 'time', 'datetime', 'temp1', 'temp2', 'temp3', 'temp4',
                  'moisture', 'humidity', 'pressure', 'light']
        for row in result:
            dataitem = {}
            index = 0
            for col in row:
                dataitem[labels[index]] = col
                index += 1
            data.append(dataitem)

    return render_template('daychart.html', source_ip = source_ip, source_ips = source_ips, date = date, dates = dates, data = data )

@app.route('/monthchart', methods=['GET'])
def monthchart():
    logging.info('Handle request for /monthchart.html')

    # create connection to our database
    dbfilename = "envplatdata.db"
    mydb = db.createConnection(dbfilename)
    cursor = mydb.cursor()
    sql = '''select distinct date from datapoints order by date desc'''
    result = cursor.execute(sql).fetchall()
    dates = []
    for item in result:
        for subitem in item:
            dates.append(subitem)

    sql = '''select distinct source_ip from datapoints order by source_ip asc'''
    result = cursor.execute(sql).fetchall()
    source_ips = []
    for item in result:
        for subitem in item:
            source_ips.append(subitem)

    data = []

    source_ip = request.args.get('source_ip')
    if source_ip == None:
        source_ip = source_ips[0]

    sql = '''select * from datapoints where source_ip is ? order by date asc'''
    result = cursor.execute(sql, (source_ip, )).fetchall()

    labels = ['id', 'source_ip' , 'date', 'time', 'datetime', 'temp1', 'temp2', 'temp3', 'temp4',
              'moisture', 'humidity', 'pressure', 'light']
    for row in result:
        dataitem = {}
        index = 0
        for col in row:
            dataitem[labels[index]] = col
            index += 1

        if dataitem['date'] > "2021-01-01":
            data.append(dataitem)
            print(dataitem)

    return render_template('monthchart.html', source_ip = source_ip, source_ips = source_ips, dates = dates, data = data )
