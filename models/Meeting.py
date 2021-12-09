from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Meeting(Base):
   __tablename__ = 'meeting_calendar'
   meeting_id = Column(Integer, primary_key=True)
   meeting_name = Column(String(length=100))
   meeting_date = Column(Date)
   meeting_start_time = Column(Time)
   meeting_end_time = Column(Time)
   agendas = relationship("Agenda")