import sys

import sqlalchemy
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import mariadb

from Agenda import Agenda

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
    return render_template('agenda_view.html')



engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3306/sgtdevsaser")

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def addAgendaToDb(meetingName, meetingDate, startTime, endTime, location, chairperson, attendees, byInvitation, apologies, minuteTaker, nextMeetingDate):
   newAgenda = Agenda(
                      date=meetingDate,
                      start_time=startTime,
                      end_time=endTime,
                      location=location,
                      chairperson=chairperson,
                      attendees=attendees,
                      by_invitation=byInvitation,
                      apologies_declines=apologies,
                      minute_taker=minuteTaker,
                      next_meeting_date=nextMeetingDate)
   session.add(newAgenda)
   session.commit()

def selectAllAgendas():
   agendas = session.query(Agenda).all()
   for agenda in agendas:
       print("Agenda ID: {}".format(agenda.agenda_id))
   return agendas


def getAgendaByDate(date):
   agendas = session.query(Agenda).filter_by(date=date)
   for agenda in agendas:
       return agenda


def updateAgenda(id, agendaView):
   agenda = session.query(Agenda).get(id)
   agenda.chairperson = agendaView.chairperson
   session.commit()

def deleteAgenda(id):
   session.query(Agenda).filter(Agenda.agenda_id == id).delete()
   session.commit()



@main.route('/getAgendas', methods=['POST', 'GET'])
def getAgenda():
    agendas = selectAllAgendas()
    return agendas


@main.route('/viewAgendaByDate', methods=['POST', 'GET'])
def viewAgendaByDate():

    date = request.form['date']
    agenda = getAgendaByDate(date)

    return render_template('agenda_view.html',
                           meetingName="SGT SASER",
                           startTime=agenda.start_time,
                           endTime=agenda.end_time,
                           location=agenda.location,
                           chairperson=agenda.chairperson,
                           attendees=agenda.attendees,
                           byInvitation=agenda.by_invitation,
                           apologies=agenda.apologies_declines,
                           minuteTaker=agenda.minute_taker,
                           date=agenda.date,
                           nextMeetingDate=agenda.next_meeting_date
                           )

@main.route('/addAgenda', methods=['POST', 'GET'])
def addAgenda():

    meetingName = request.form['name']
    meetingDate = request.form['date']
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    location = request.form['locroom']
    chairperson = request.form['chairperson']
    attendees = request.form['attendees']
    byInvite = request.form['byinvite']
    apologies = request.form['apol']
    minuteTaker = request.form['mintaker']
    nextMeetingDate = request.form['nextdate']

    addAgendaToDb(meetingName, meetingDate, startTime, endTime, location, chairperson, attendees, byInvite, apologies, minuteTaker, nextMeetingDate)


    return render_template('agenda_set.html')


main.run(debug=True)