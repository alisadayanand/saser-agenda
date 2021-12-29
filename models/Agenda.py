from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship

from models.Base import Base


class Agenda(Base):
    __tablename__ = 'agenda'
    agenda_id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meeting_calendar.meeting_id'))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    location = Column(String(length=30))
    chairperson = Column(String(length=100))
    attendees = Column(String(length=1000))
    by_invitation = Column(String(length=1000))
    apologies_declines = Column(String(length=1000))
    minute_taker = Column(String(length=100))
    next_meeting_date = Column(Date)
    meeting = relationship('Meeting', remote_side='Meeting.meeting_id')
    agenda_topics = relationship('Agenda_Topics', backref='agenda', lazy='select')

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'agenda_id': self.agenda_id,
            'meeting_id': self.meeting_id,
            'date': dump_datetime(self.date),
            'start_time': dump_datetime(self.start_time),
            'end_time': dump_datetime(self.end_time),
            'location': self.location,
            'chairperson': self.chairperson,
            'attendees': self.attendees,
            'by_invitation': self.by_invitation,
            'apologies_declines': self.apologies_declines,
            'minute_taker': self.minute_taker,
            'next_meeting_date': dump_datetime(self.next_meeting_date)
        }


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
