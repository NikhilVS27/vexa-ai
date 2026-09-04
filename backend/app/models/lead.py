from sqlalchemy import Column, Integer, String, Boolean, Text

from backend.app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    brand_name = Column(
        String(255),
        nullable=False
    )

    lead_type = Column(
        String(100),
        nullable=False
    )

    priority = Column(
        String(50),
        nullable=False
    )

    opportunity_score = Column(
        Integer,
        default=0
    )

    gaming_signal = Column(
        Boolean,
        default=False
    )

    sponsorship_signal = Column(
        Boolean,
        default=False
    )

    # AI analysis fields

    industry = Column(
        String(255)
    )

    gaming_activity = Column(
        Boolean,
        default=False
    )

    sponsorship_activity = Column(
        Boolean,
        default=False
    )

    opportunity = Column(
        Text
    )

    reasoning = Column(
        Text
    )

    # Article information

    title = Column(
        String(500)
    )

    description = Column(
        Text
    )

    published_at = Column(
        String(100)
    )

    source_url = Column(
        Text
    )

    source_count = Column(
        Integer,
        default=1
    )