from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.lead import Lead


router = APIRouter(
    prefix="/api/leads",
    tags=["Leads"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def lead_to_dict(lead: Lead):
    """
    Convert a Lead database object
    into a JSON-friendly dictionary.
    """

    return {
        "id": lead.id,

        "brand_name": lead.brand_name,

        "lead_type": lead.lead_type,

        "priority": lead.priority,

        "opportunity_score": (
            lead.opportunity_score
        ),

        "industry": lead.industry,

        "gaming_signal": (
            lead.gaming_signal
        ),

        "sponsorship_signal": (
            lead.sponsorship_signal
        ),

        "gaming_activity": (
            lead.gaming_activity
        ),

        "sponsorship_activity": (
            lead.sponsorship_activity
        ),

        "opportunity": (
            lead.opportunity
        ),

        "reasoning": (
            lead.reasoning
        ),

        "title": lead.title,

        "description": lead.description,

        "published_at": (
            lead.published_at
        ),

        "source_url": (
            lead.source_url
        ),

        "source_count": (
            lead.source_count
        )
    }


@router.get("/")
def get_leads(
    priority: str | None = None,
    lead_type: str | None = None,
    gaming_signal: bool | None = None,
    min_score: int | None = None,
    db: Session = Depends(get_db)
):
    """
    Return leads with optional filters.
    """

    query = db.query(Lead)

    # Priority filter
    if priority:

        query = query.filter(
            Lead.priority == priority
        )

    # Lead type filter
    if lead_type:

        query = query.filter(
            Lead.lead_type == lead_type
        )

    # Gaming signal filter
    if gaming_signal is not None:

        query = query.filter(
            Lead.gaming_signal == gaming_signal
        )

    # Minimum opportunity score
    if min_score is not None:

        query = query.filter(
            Lead.opportunity_score >= min_score
        )

    # Highest opportunity first
    leads = (
        query
        .order_by(
            Lead.opportunity_score.desc(),
            Lead.id.desc()
        )
        .all()
    )

    return [
        lead_to_dict(lead)
        for lead in leads
    ]


@router.get("/{lead_id}")
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Return a single lead by ID.
    """

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )

    if not lead:

        return {
            "error": "Lead not found"
        }

    return lead_to_dict(
        lead
    )