from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from datetime import datetime

from database import Base

class UserConfiguration(Base):
    __tablename__ = "user_configurations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    config_id = Column(Integer, ForeignKey("configurations.id"))
    access_granted_at = Column(DateTime, default=datetime.now)