def calculate_opportunity_score(lead: dict) -> int:
    """
    Calculate a prototype opportunity score
    between 0 and 100.
    """

    score = 0

    # Gaming activity
    if lead.get("gaming_signal"):
        score += 25

    # Sponsorship activity
    if lead.get("sponsorship_signal"):
        score += 25

    # Strong gaming-related keywords
    title = (
        lead.get("title") or ""
    ).lower()

    description = (
        lead.get("description") or ""
    ).lower()

    text = title + " " + description

    strong_gaming_keywords = [
        "esports partnership",
        "gaming partnership",
        "esports sponsor",
        "gaming sponsor",
        "title sponsor",
        "esports campaign",
        "gaming campaign",
        "esports world cup",
        "s8ul"
    ]

    if any(
        keyword in text
        for keyword in strong_gaming_keywords
    ):
        score += 15

    # Additional gaming keyword signal
    gaming_keywords = [
        "esports",
        "gaming",
        "gamer",
        "gaming team",
        "esports team",
        "tournament",
        "bgmi",
        "valorant",
        "free fire"
    ]

    if any(
        keyword in text
        for keyword in gaming_keywords
    ):
        score += 10

    # Multiple sources indicate stronger evidence
    source_count = lead.get(
        "source_count",
        1
    )

    if source_count >= 3:
        score += 10

    # Existing gaming sponsor
    if (
        lead.get("lead_type")
        == "Existing Gaming Sponsor"
    ):
        score += 15

    # Make sure score never exceeds 100
    score = min(score, 100)

    return score


def get_priority_from_score(
    score: int
) -> str:
    """
    Convert opportunity score into
    a priority level.
    """

    if score >= 80:
        return "High"

    if score >= 60:
        return "Medium"

    return "Low"


def analyze_lead(lead: dict) -> dict:
    """
    Calculate the opportunity score
    and priority for a lead.
    """

    score = calculate_opportunity_score(
        lead
    )

    priority = get_priority_from_score(
        score
    )

    return {
        "opportunity_score": score,
        "priority": priority
    }


if __name__ == "__main__":

    # Test lead
    test_lead = {
        "brand_name": "Campa Energy",
        "lead_type": "Existing Gaming Sponsor",
        "gaming_signal": True,
        "sponsorship_signal": True,
        "title": (
            "Campa Energy Becomes Title Sponsor "
            "for S8UL EWC 2026 Campaign"
        ),
        "description": (
            "Campa Energy partners with S8UL "
            "for the Esports World Cup campaign."
        ),
        "source_count": 4
    }

    result = analyze_lead(
        test_lead
    )

    print(
        "===== LEAD SCORE TEST ====="
    )

    print(
        "Brand:",
        test_lead["brand_name"]
    )

    print(
        "Opportunity Score:",
        result["opportunity_score"]
    )

    print(
        "Priority:",
        result["priority"]
    )