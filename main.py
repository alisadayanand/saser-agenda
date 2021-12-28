from flask import Flask, render_template, request

from models.Agenda import Agenda
from models.Agenda_Topics import Agenda_Topics
from models.Meeting import Meeting
from models.Base import Session

session = Session()
selectedEditAgenda = ''
page_state = ''

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


def addAgendaAndTopicsToDb(newAgenda, newTopic):

    session.add(newAgenda)
    session.flush()

    session.refresh(newAgenda)

    newTopic.agenda_id = newAgenda.agenda_id
    newTopic.minutes_id = 1

    session.add(newTopic)
    session.commit()


def selectAllAgendas():
    return session.query(Agenda).all()


def getAgendaByDate(date):
    return session.query(Agenda).filter_by(date=date).first()


def updateAgendaInDb(id, topic_id, agendaView, topicView):

    agenda = session.query(Agenda).filter(Agenda.agenda_id == id).first()
    topic = session.query(Agenda_Topics).filter(Agenda_Topics.topic_id == topic_id).first()


    agenda.date = agendaView.date
    agenda.start_time = agendaView.start_time
    agenda.end_time = agendaView.end_time
    agenda.location = agendaView.location
    agenda.chairperson = agendaView.chairperson
    agenda.attendees = agendaView.attendees
    agenda.by_invitation = agendaView.by_invitation
    agenda.apologies_declines = agendaView.apologies_declines
    agenda.minute_taker = agendaView.minute_taker
    agenda.next_meeting_date = agendaView.next_meeting_date

    topic.minutes_id = id
    topic.topic_name = topicView.topic_name
    topic.agenda_id = id
    topic.topic_owner = topicView.topic_owner
    topic.ForAwareness = topicView.ForAwareness
    topic.RfProcess = topicView.RfProcess
    topic.RiskManagement = topicView.RiskManagement
    topic.ForInput = topicView.ForInput
    topic.ForApproval = topicView.ForApproval

    session.add(agenda)
    session.commit()

    session.add(topic)
    session.commit()


def deleteAgenda(id):
    session.query(Agenda).filter(Agenda.agenda_id == id).delete()
    session.commit()

def deleteTopic(id):
    session.query(Agenda_Topics).filter(Agenda_Topics.topic_id == id).delete()
    session.commit()


def selectAllMeetings():
    meetings = session.query(Meeting).all()
    for meeting in meetings:
        print("Meeting ID: {}".format(meeting.meeting_id))
    return meetings


def selectAllAgenda_Topics():
    return session.query(Agenda_Topics).all()


@main.route('/getAgenda_Topics', methods=['POST', 'GET'])
def getAgenda_Topics():
    return selectAllAgenda_Topics()


@main.route('/getAgendas', methods=['POST', 'GET'])
def getAgenda():
    agendas = selectAllAgendas()
    return agendas


@main.route('/viewAgendaByDate', methods=['POST', 'GET'])
def viewAgendaByDate():
    headings = (
    'Topics', 'For Awareness', 'RF Process or Vendor Selection', 'Risk Management', 'For Input', 'For Approval',
    'Owner')

    date = request.form['date']
    agenda = getAgendaByDate(date)

    # set as a global variable so that I can get the id
    global selectedEditAgenda
    selectedEditAgenda = agenda

    global page_state

    if request.referrer == 'http://localhost:5000/view' or request.referrer == 'http://localhost:5000/edit':
        page_state = request.referrer

    if page_state == 'http://localhost:5000/view':

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
                               nextMeetingDate=agenda.next_meeting_date,
                               headings=headings,
                               agenda_topics=agenda.agenda_topics
                               )

    else:

        return render_template('agenda_edit.html',
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
                               nextMeetingDate=agenda.next_meeting_date,
                               headings=headings,
                               agenda_topics=agenda.agenda_topics
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

    newAgenda = Agenda(
        meeting_id=1,
        date=meetingDate,
        start_time=startTime,
        end_time=endTime,
        location=location,
        chairperson=chairperson,
        attendees=attendees,
        by_invitation=byInvite,
        apologies_declines=apologies,
        minute_taker=minuteTaker,
        next_meeting_date=nextMeetingDate)

    topicName = request.form['topic']
    topicAwareness = request.form['aware']
    topicRf = request.form['rf']
    topicRiskManagement = request.form['risk']
    topicInput = request.form['input']
    topicApproval = request.form['approve']
    topicOwner = request.form['owner']

    newTopic = Agenda_Topics(topic_name=topicName,
                             topic_owner=topicOwner,
                             ForAwareness=topicAwareness,
                             RfProcess=topicRf,
                             RiskManagement=topicRiskManagement,
                             ForInput=topicInput,
                             ForApproval=topicApproval)

    addAgendaAndTopicsToDb(newAgenda, newTopic)

    return render_template('agenda_set.html')


@main.route('/updateAgenda', methods=['POST', 'GET'])
def updateAgenda():
    global selectedEditAgenda
    meetingName = request.form['name']
    meetingDate = selectedEditAgenda.date
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    location = request.form['locroom']
    chairperson = request.form['chairperson']
    attendees = request.form['attendees']
    byInvite = request.form['byinvite']
    apologies = request.form['apol']
    minuteTaker = request.form['mintaker']
    nextMeetingDate = request.form['nextdate']

    # topics to be saved with the agenda
    topicName = request.form['topic']
    topicAwareness = request.form['aware']
    topicRf = request.form['rf']
    topicRiskManagement = request.form['risk']
    topicInput = request.form['input']
    topicApproval = request.form['approve']
    topicOwner = request.form['owner']
    topicId = request.form['hiddenTopicId']

    # topicUpdated = Agenda_Topics(topic_id=int(topicId),
    #                              agenda_id=selectedEditAgenda.agenda_id,
    #                              minutes_id=1,
    #                              topic_name=topicName,
    #                              topic_owner=topicOwner,
    #                              ForAwareness=topicAwareness,
    #                              RfProcess=topicRf,
    #                              RiskManagement=topicRiskManagement,
    #                              ForInput=topicInput,
    #                              ForApproval=topicApproval,
    #                              agenda=selectedEditAgenda)

    topicUpdated = Agenda_Topics(agenda_id=selectedEditAgenda.agenda_id,
                                 minutes_id=1,
                                 topic_name=topicName,
                                 topic_owner=topicOwner,
                                 ForAwareness=topicAwareness,
                                 RfProcess=topicRf,
                                 RiskManagement=topicRiskManagement,
                                 ForInput=topicInput,
                                 ForApproval=topicApproval)

    agendaUpdated = Agenda(
        date=meetingDate,
        start_time=startTime,
        end_time=endTime,
        location=location,
        chairperson=chairperson,
        attendees=attendees,
        by_invitation=byInvite,
        apologies_declines=apologies,
        minute_taker=minuteTaker,
        next_meeting_date=nextMeetingDate)

    updateAgendaInDb(selectedEditAgenda.agenda_id, topicId, agendaUpdated, topicUpdated)


@main.route('/getMeetings', methods=['POST', 'GET'])
def getMeetings():
    meetings = selectAllMeetings()
    return meetings


main.run(debug=True)
