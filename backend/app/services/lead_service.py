from sqlalchemy.orm import Session

from backend.app.models.lead import Lead


def save_lead(
    db: Session,
    lead_data: dict
):
    """
    Save a discovered lead into PostgreSQL.
    """

    brand_name = lead_data.get(
        "brand_name",
        "Unknown"
    )

    source_url = lead_data.get(
        "source_url"
    )

    # Check whether this exact source
    # already exists.
    existing_lead = (
        db.query(Lead)
        .filter(
            Lead.source_url == source_url
        )
        .first()
    )

    if existing_lead:

        # Update existing lead
        existing_lead.brand_name = brand_name

        existing_lead.lead_type = lead_data.get(
            "lead_type",
            "Unclassified"
        )

        existing_lead.priority = lead_data.get(
            "priority",
            "Low"
        )

        existing_lead.opportunity_score = lead_data.get(
            "opportunity_score",
            0
        )

        existing_lead.gaming_signal = lead_data.get(
            "gaming_signal",
            False
        )

        existing_lead.sponsorship_signal = lead_data.get(
            "sponsorship_signal",
            False
        )

        # AI analysis fields
        existing_lead.industry = lead_data.get(
            "industry"
        )

        existing_lead.gaming_activity = lead_data.get(
            "gaming_activity",
            False
        )

        existing_lead.sponsorship_activity = lead_data.get(
            "sponsorship_activity",
            False
        )

        existing_lead.opportunity = lead_data.get(
            "opportunity"
        )

        existing_lead.reasoning = lead_data.get(
            "reasoning"
        )

        # Article information
        existing_lead.title = lead_data.get(
            "title"
        )

        existing_lead.description = lead_data.get(
            "description"
        )

        existing_lead.published_at = lead_data.get(
            "published_at"
        )

        existing_lead.source_count = lead_data.get(
            "source_count",
            1
        )

        db.commit()
        db.refresh(existing_lead)

        return existing_lead

    # Create new lead
    new_lead = Lead(
        brand_name=brand_name,

        lead_type=lead_data.get(
            "lead_type",
            "Unclassified"
        ),

        priority=lead_data.get(
            "priority",
            "Low"
        ),

        opportunity_score=lead_data.get(
            "opportunity_score",
            0
        ),

        gaming_signal=lead_data.get(
            "gaming_signal",
            False
        ),

        sponsorship_signal=lead_data.get(
            "sponsorship_signal",
            False
        ),

        # AI analysis fields
        industry=lead_data.get(
            "industry"
        ),

        gaming_activity=lead_data.get(
            "gaming_activity",
            False
        ),

        sponsorship_activity=lead_data.get(
            "sponsorship_activity",
            False
        ),

        opportunity=lead_data.get(
            "opportunity"
        ),

        reasoning=lead_data.get(
            "reasoning"
        ),

        # Article information
        title=lead_data.get(
            "title"
        ),

        description=lead_data.get(
            "description"
        ),

        published_at=lead_data.get(
            "published_at"
        ),

        source_url=source_url,

        source_count=lead_data.get(
            "source_count",
            1
        )
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead