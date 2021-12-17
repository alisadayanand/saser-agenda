from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.Base import Base


class Agenda_Topics(Base):
   __tablename__ = 'agenda_topics'
   topic_id = Column(Integer, primary_key=True)
   agenda_id = Column(Integer, ForeignKey('agenda.agenda_id'))
   minutes_id = Column(Integer)
   topic_name = Column(String(length=100))
   topic_owner = Column(String(length=100))
   ForAwareness = Column(String(length=100))
   RfProcess = Column(String(length=100))
   RiskManagement = Column(String(length=100))
   ForInput = Column(String(length=100))
   ForApproval = Column(String(length=100))
   agenda = relationship("Agenda", back_populates="agenda_topics")


