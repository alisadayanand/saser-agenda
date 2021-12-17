from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.Base import Base


class Agenda_Topics(Base):
   __tablename__ = 'agenda_topics'
   topic_id = Column(Integer, primary_key=True)
   agenda_id = Column(Integer, ForeignKey('agenda.agenda_id'))
   minutes_id = Column(Integer)
   topic_name = Column(String(length=100))
   topic_owner = Column(String(length=100))
   ForAwareness = Column(Boolean)
   RfProcess = Column(Boolean)
   RiskManagement = Column(Boolean)
   ForInput = Column(Boolean)
   ForApproval = Column(Boolean)
   # meeting = relationship('Meeting', remote_side='Meeting.meeting_id')
   # agendas = relationship("Agenda", back_populates='agenda_topics')
   agenda = relationship("Agenda", back_populates="agenda_topics")


