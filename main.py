import sys

from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import mariadb


main = Flask(__name__)

@main.route('/home', methods=['POST', 'GET'])
@main.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@main.route('/set', methods=['POST', 'GET'])
def set():
    return render_template('agenda_set.html')

@main.route('/edit', methods=['POST', 'GET'])
def edit():
    return render_template('agenda_edit.html')

@main.route('/view', methods=['POST', 'GET'])
def view():
    return render_template('agenda_view.html', test="fdsfsdfsf")



# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",  # Username
        password="root",  # Password
        host="127.0.0.1",  # Host IP
        port=3306,
        database="sgtdevsaser"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

@main.route('/getAgenda', methods=['POST', 'GET'])
def getAgenda():

    result = []
    script = """SELECT * FROM sgtdevsaser.agenda"""
    cs = conn.cursor()
    cs.execute(script)
    for row in cs:
        result.append(row)

    print(result)
    return str(result)


@main.route('/viewAgendaByDate', methods=['POST', 'GET'])
def viewAgendaByDate():

    date = request.form['date']
    print(date)

    result = []
    script = """SELECT * FROM sgtdevsaser.agenda WHERE date = '{}'""".format(date)
    cs = conn.cursor()
    cs.execute(script)
    for row in cs:
        result.append(row)

    print(result)
    # return str(result)

    # [(1, 1, datetime.date(2021, 12, 10), datetime.timedelta(seconds=39600), datetime.timedelta(seconds=46800),
    #   'Microsoft Teams', 'Craig Cadenhead', 'Courtley Whittaker (SGT)', 'Edwin Jacobs', 'Theo Mabaso', 'Helen Meyer',
    #   datetime.date(2021, 12, 15))]

    # for column in result:
    #
    # response = {'meetingName': 'SGT SASER',
    #             'location': }
    # return
    return render_template('agenda_view.html', location="Microsoft Teams")


main.run(debug=True)