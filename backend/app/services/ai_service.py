def analyze_brand(lead: dict) -> dict:
    """
    Prototype AI-style analysis of a discovered brand.

    This version uses the available article data and
    simple rules. Later, this function can be connected
    to an actual LLM API without changing the rest
    of the application significantly.
    """

    brand_name = lead.get(
        "brand_name",
        "Unknown"
    )

    title = (
        lead.get("title") or ""
    )

    description = (
        lead.get("description") or ""
    )

    text = (
        title + " " + description
    ).lower()

    # --------------------------------
    # Industry detection
    # --------------------------------

    industry = "Unknown"

    industry_keywords = {

        "FMCG / Beverages": [
            "energy drink",
            "beverage",
            "drink",
            "cola",
            "campa",
            "pepsi",
            "coca-cola",
            "red bull",
            "monster"
        ],

        "Technology": [
            "technology",
            "tech",
            "software",
            "ai",
            "artificial intelligence",
            "cloud",
            "semiconductor",
            "processor",
            "laptop",
            "smartphone"
        ],

        "Consumer Electronics": [
            "smartphone",
            "mobile phone",
            "laptop",
            "headphones",
            "earbuds",
            "electronics",
            "gaming device"
        ],

        "Automotive": [
            "automobile",
            "automotive",
            "car",
            "cars",
            "vehicle",
            "motorcycle",
            "bike"
        ],

        "Financial Services": [
            "bank",
            "banking",
            "finance",
            "financial",
            "fintech",
            "credit card",
            "payment"
        ],

        "Fashion": [
            "fashion",
            "clothing",
            "apparel",
            "sneakers",
            "shoes",
            "streetwear"
        ],

        "Food": [
            "food",
            "restaurant",
            "snack",
            "snacks",
            "pizza",
            "burger"
        ]
    }

    for industry_name, keywords in (
        industry_keywords.items()
    ):

        if any(
            keyword in text
            for keyword in keywords
        ):

            industry = industry_name
            break

    # --------------------------------
    # Gaming activity
    # --------------------------------

    gaming_keywords = [
        "gaming",
        "esports",
        "e-sports",
        "gamer",
        "gaming team",
        "esports team",
        "gaming creator",
        "esports athlete",
        "tournament",
        "bgmi",
        "valorant",
        "free fire",
        "esports world cup",
        "ewc"
    ]

    gaming_activity = any(
        keyword in text
        for keyword in gaming_keywords
    )

    # --------------------------------
    # Sponsorship activity
    # --------------------------------

    sponsorship_keywords = [
        "sponsor",
        "sponsorship",
        "title sponsor",
        "sponsored",
        "partnership",
        "partner",
        "collaboration"
    ]

    sponsorship_activity = any(
        keyword in text
        for keyword in sponsorship_keywords
    )

    # --------------------------------
    # Lead opportunity
    # --------------------------------

    if (
        gaming_activity
        and sponsorship_activity
    ):

        opportunity = (
            "Strong gaming sponsorship opportunity"
        )

    elif gaming_activity:

        opportunity = (
            "Potential gaming partnership opportunity"
        )

    elif sponsorship_activity:

        opportunity = (
            "Potential sponsorship opportunity"
        )

    else:

        opportunity = (
            "Low-confidence opportunity"
        )

    # --------------------------------
    # Reasoning
    # --------------------------------

    reasons = []

    if gaming_activity:

        reasons.append(
            "Recent gaming or esports activity detected"
        )

    if sponsorship_activity:

        reasons.append(
            "Recent sponsorship or partnership activity detected"
        )

    if industry != "Unknown":

        reasons.append(
            f"Brand appears to operate in the {industry} industry"
        )

    if not reasons:

        reasons.append(
            "Limited commercial signals detected in the article"
        )

    reasoning = ". ".join(
        reasons
    ) + "."

    return {
        "brand_name": brand_name,
        "industry": industry,
        "gaming_activity": gaming_activity,
        "sponsorship_activity": sponsorship_activity,
        "opportunity": opportunity,
        "reasoning": reasoning
    }


if __name__ == "__main__":

    test_lead = {

        "brand_name": "Campa Energy",

        "title": (
            "Campa Energy Becomes Title Sponsor "
            "for S8UL EWC 2026 Campaign"
        ),

        "description": (
            "Campa Energy partners with S8UL "
            "for the Esports World Cup campaign."
        )
    }

    result = analyze_brand(
        test_lead
    )

    print(
        "===== AI ANALYSIS TEST ====="
    )

    print(
        "Brand:",
        result["brand_name"]
    )

    print(
        "Industry:",
        result["industry"]
    )

    print(
        "Gaming Activity:",
        result["gaming_activity"]
    )

    print(
        "Sponsorship Activity:",
        result["sponsorship_activity"]
    )

    print(
        "Opportunity:",
        result["opportunity"]
    )

    print(
        "Reasoning:",
        result["reasoning"]
    )

    