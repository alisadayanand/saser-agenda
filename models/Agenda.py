from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Agenda(Base):
   __tablename__ = 'agenda'
   agenda_id = Column(Integer, primary_key=True)
   meeting_id = Column(Integer, ForeignKey('meeting_id'))
   date = Column(Date)
   start_time = Column(Time)
   end_time = Column(Time)
   location = Column(String(length=100))
   chairperson = Column(String(length=100))
   attendees = Column(String(length=100))
   by_invitation = Column(String(length=100))
   apologies_declines = Column(String(length=100))
   minute_taker = Column(String(length=100))
   next_meeting_date = Column(Date)