from sqlalchemy import Column, Integer, Date, Time, String
from sqlalchemy.orm import relationship

from models.Base import Base


class Meeting(Base):
    __tablename__ = 'meeting_calendar'
    meeting_id = Column(Integer, primary_key=True)
    meeting_name = Column(String(length=100))
    meeting_date = Column(Date)
    meeting_start_time = Column(Time)
    meeting_end_time = Column(Time)
    agenda = relationship("Agenda", uselist=False, back_populates='meeting')

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'meeting_id': self.meeting_id,
            'meeting_name': self.meeting_name,
            'meeting_date': dump_datetime(self.meeting_date),
            'meeting_start_time': dump_datetime(self.meeting_start_time),
            'meeting_end_time': dump_datetime(self.meeting_end_time)
        }


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
