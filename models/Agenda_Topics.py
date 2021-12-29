from sqlalchemy import Column, Integer, String, ForeignKey

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

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'topic_id': self.topic_id,
            'agenda_id': self.agenda_id,
            'minutes_id': self.minutes_id,
            'topic_name': self.topic_name,
            'topic_owner': self.topic_owner,
            'ForAwareness': self.ForAwareness,
            'RfProcess': self.RfProcess,
            'RiskManagement': self.RiskManagement,
            'ForInput': self.ForInput,
            'ForApproval': self.ForApproval
        }


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
