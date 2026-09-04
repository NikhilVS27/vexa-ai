from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime

from backend.app.core.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False, index=True)

    website = Column(String(500), nullable=True)

    industry = Column(String(255), nullable=True)

    description = Column(Text, nullable=True)

    gaming_history = Column(Text, nullable=True)

    marketing_activity = Column(Text, nullable=True)

    opportunity_score = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )