from flask import Flask, render_template, request, flash, jsonify

from models.Agenda import Agenda
from models.Agenda_Topics import Agenda_Topics
from models.Base import Session
from models.Meeting import Meeting

session = Session()
selectedEditAgenda = ''
page_state = ''

main = Flask(__name__)

# Routes


@main.route('/home', methods=['POST', 'GET'])
@main.route('/', methods=['POST', 'GET'])
def home():
    try:
        return render_template('index.html')

    except Exception as e:
        page_not_found(e)


@main.route('/set', methods=['POST', 'GET'])
def set():
    try:
        meetings = getMeetings()
        return render_template('agenda_set.html', meetings=meetings)
        # return render_template('agenda_set.html')

    except Exception as e:
        page_not_found(e)


@main.route('/edit', methods=['POST', 'GET'])
def edit():
    try:
        return render_template('agenda_edit.html')

    except Exception as e:
        page_not_found(e)


@main.route('/view', methods=['POST', 'GET'])
def view():
    try:
        return render_template('agenda_view.html')

    except Exception as e:
        page_not_found(e)


@main.route('/getAgenda_Topics', methods=['POST', 'GET'])
def getAgenda_Topics():
    return jsonify(topics=[topic.serialize for topic in selectAllAgenda_Topics()])


@main.route('/getAgendas', methods=['POST', 'GET'])
def getAgenda():
    agendas = selectAllAgendas()
    return jsonify(agendas=[agenda.serialize for agenda in agendas])


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
        try:
            if not agenda:
                flash("No agenda found for this date", "warning")
                return render_template('agenda_view.html')

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
        except Exception as e:
            page_not_found(e)

    else:
        try:
            if not agenda:
                flash("No agenda found for this date", "warning")
                return render_template('agenda_edit.html')

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
        except Exception as e:
            page_not_found(e)


@main.route('/addAgenda', methods=['POST', 'GET'])
def addAgenda():
    # meetingId = request.form['hiddenMeetingId']
    meetingId = request.form['name']
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
        meeting_id=meetingId,
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

    try:
        flash("Agenda created successfully", "success")
        return render_template('agenda_set.html', meetings=getMeetings())

    except Exception as e:
        page_not_found(e)


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

    try:
        flash("Agenda edited successfully", "success")
        return render_template("agenda_edit.html")

    except Exception as e:
        page_not_found(e)


@main.route('/getMeetings', methods=['POST', 'GET'])
def getMeetings():
    meetings = selectAllMeetings()
    # return jsonify(meetings=[meeting.serialize for meeting in meetings])
    return meetings


@main.route('/getMeetingsWithView', methods=['POST', 'GET'])
def getMeetingsWithView():
    date = request.form["date"]
    meeting = getMeetingByDate(date)
    return render_template("agenda_set.html", agenda=meeting.agenda)

@main.errorhandler(404)
def page_not_found(e):
    flash("404 page not found", "danger")
    return render_template("404.html")


# CRUD

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

    topic.minutes_id = 1
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

def getMeetingByDate(date):
    return session.query(Meeting).filter_by(meeting_date=date).first()


def selectAllAgenda_Topics():
    return session.query(Agenda_Topics).all()

if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    main.secret_key = 'super secret key'
    main.config['SESSION_TYPE'] = 'filesystem'

    main.run(debug=True)


# TODO:
#
#  attendees spelling error (DONE)
#
# error messages when view or edit wrong date (DONE)
#
# success message when setting new agenda (DONE)
#
# error handling blank fields (DONE)
#
# max varchar text fields in backend
#
# meeting id dropdown in set agenda. Frontend and backend