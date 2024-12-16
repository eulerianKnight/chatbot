from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime

from database import Base

class Configuration(Base):
    __tablename__ = "configurations"
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    agent_name = Column(String(255))
    max_tokens = Column(Integer)
    top_p = Column(Float)
    model = Column(String(50))
    tools = Column(String(50))
    temperature = Column(Float)
    presence_penalty = Column(Float)
    frequency_penalty = Column(Float)
    system_prompt = Column(String(50))
    agent_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)