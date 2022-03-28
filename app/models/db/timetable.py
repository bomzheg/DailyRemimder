from sqlalchemy import Column, Text, BigInteger, ForeignKey, Time, ARRAY
from sqlalchemy.orm import relationship

from app.models.db.base import Base


class Timetable(Base):
    __tablename__ = "timetables"
    __mapper_args__ = {"eager_defaults": True}
    id = Column(BigInteger, primary_key=True)
    time = Column(Time)
    weekdays = Column(ARRAY(Text))
    meeting_id = Column(BigInteger, ForeignKey("meetings.id"))
    meeting = relationship("Meeting", back_populates="timetables")
