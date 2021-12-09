import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Agenda(Base):
   __tablename__ = 'agenda'
   agenda_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
   meeting_id = sqlalchemy.Column(sqlalchemy.Integer)
   date = sqlalchemy.Column(sqlalchemy.Date)
   start_time = sqlalchemy.Column(sqlalchemy.Time)
   end_time = sqlalchemy.Column(sqlalchemy.Time)
   location = sqlalchemy.Column(sqlalchemy.String(length=100))
   chairperson = sqlalchemy.Column(sqlalchemy.String(length=100))
   attendees = sqlalchemy.Column(sqlalchemy.String(length=100))
   by_invitation = sqlalchemy.Column(sqlalchemy.String(length=100))
   apologies_declines = sqlalchemy.Column(sqlalchemy.String(length=100))
   minute_taker = sqlalchemy.Column(sqlalchemy.String(length=100))
   next_meeting_date = sqlalchemy.Column(sqlalchemy.Date)