import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from backend.app.core.database import SessionLocal
from backend.app.services.lead_service import save_lead
from backend.app.services.scoring_service import analyze_lead
from backend.app.services.ai_service import analyze_brand


# ==========================================
# REQUEST HEADERS
# ==========================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


# ==========================================
# DISCOVER NEWS
# ==========================================

def discover_news(query: str, max_results: int = 10):
    """
    Discover recent articles using Google News RSS.

    Multiple queries are used so that the discovery
    engine has a better chance of finding results.
    """

    search_queries = [
        query,
        "India esports sponsorship",
        "gaming sponsorship India brands",
        "esports brands India",
        "gaming partnership India",
    ]

    all_articles = []
    seen_urls = set()

    for search_query in search_queries:

        print(
            f"Searching Google News for: {search_query}"
        )

        encoded_query = quote(search_query)

        rss_url = (
            "https://news.google.com/rss/search"
            f"?q={encoded_query}"
            "&hl=en-IN"
            "&gl=IN"
            "&ceid=IN:en"
        )

        try:

            response = requests.get(
                rss_url,
                headers=HEADERS,
                timeout=15
            )

            print(
                f"Google News response: {response.status_code}"
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.content,
                "xml"
            )

            items = soup.find_all("item")

            print(
                f"Articles returned: {len(items)}"
            )

            for item in items:

                if len(all_articles) >= max_results:
                    break

                title_tag = item.find("title")
                link_tag = item.find("link")
                description_tag = item.find(
                    "description"
                )
                pub_date_tag = item.find(
                    "pubDate"
                )

                title = (
                    title_tag.get_text(
                        strip=True
                    )
                    if title_tag
                    else None
                )

                url = (
                    link_tag.get_text(
                        strip=True
                    )
                    if link_tag
                    else None
                )

                description = (
                    description_tag.get_text(
                        " ",
                        strip=True
                    )
                    if description_tag
                    else None
                )

                published_at = (
                    pub_date_tag.get_text(
                        strip=True
                    )
                    if pub_date_tag
                    else None
                )

                if not title or not url:
                    continue

                if url in seen_urls:
                    continue

                seen_urls.add(url)

                all_articles.append(
                    {
                        "title": title,
                        "url": url,
                        "description": description,
                        "published_at": published_at
                    }
                )

            if len(all_articles) >= max_results:
                break

        except requests.RequestException as e:

            print(
                f"Google News request failed: {e}"
            )

        except Exception as e:

            print(
                f"Error processing Google News response: {e}"
            )

    return all_articles[:max_results]


# ==========================================
# CLEAN NEWS ARTICLE
# ==========================================

def clean_news_article(article):
    """
    Remove HTML from article descriptions.
    """

    title = article.get("title")
    description = article.get("description")

    if description:

        description_soup = BeautifulSoup(
            description,
            "html.parser"
        )

        clean_description = (
            description_soup.get_text(
                " ",
                strip=True
            )
        )

    else:

        clean_description = ""

    return {
        "title": title,
        "url": article.get("url"),
        "published_at": article.get(
            "published_at"
        ),
        "description": clean_description
    }


# ==========================================
# CLASSIFY LEAD
# ==========================================

def classify_lead(article):
    """
    Classify an article into a basic lead type.
    """

    title = article.get("title") or ""
    description = article.get("description") or ""

    text = (
        title + " " + description
    ).lower()

    sponsorship_keywords = [
        "sponsor",
        "sponsorship",
        "title sponsor",
        "sponsored",
        "partnership",
        "partner",
        "collaboration"
    ]

    gaming_keywords = [
        "gaming",
        "esports",
        "e-sports",
        "gamer",
        "s8ul",
        "ewc",
        "esports world cup",
        "gaming team",
        "esports team",
        "gaming creator",
        "esports athlete",
        "tournament",
        "bgmi",
        "valorant",
        "free fire",
        "league"
    ]

    sponsorship_found = any(
        keyword in text
        for keyword in sponsorship_keywords
    )

    gaming_found = any(
        keyword in text
        for keyword in gaming_keywords
    )

    if (
        sponsorship_found
        and gaming_found
    ):

        lead_type = "Existing Gaming Sponsor"
        priority = "High"

    elif gaming_found:

        lead_type = "Gaming-Related Brand"
        priority = "Medium"

    elif sponsorship_found:

        lead_type = "Potential Sponsor"
        priority = "Medium"

    else:

        lead_type = "Unclassified"
        priority = "Low"

    return {
        "lead_type": lead_type,
        "priority": priority,
        "gaming_signal": gaming_found,
        "sponsorship_signal": sponsorship_found
    }


# ==========================================
# EXTRACT BRAND NAME
# ==========================================

def extract_brand_name(article):
    """
    Extract a known brand name from the article title.
    """

    title = article.get("title") or ""
    title_lower = title.lower()

    known_brands = [
        "Campa Energy",
        "Red Bull",
        "Monster Energy",
        "Mountain Dew",
        "Samsung",
        "Realme",
        "OnePlus",
        "AMD",
        "Intel",
        "Lenovo",
        "HP",
        "Acer",
        "ASUS",
        "boAt"
    ]

    for brand in known_brands:

        if brand.lower() in title_lower:

            return brand

    patterns = [
        " becomes title sponsor",
        " becomes the title sponsor",
        " named title sponsor",
        " is title sponsor",
        " joins as sponsor",
        " joins as a sponsor",
        " signs sponsorship",
        " announces sponsorship"
    ]

    for pattern in patterns:

        position = title_lower.find(
            pattern
        )

        if position > 0:

            possible_brand = (
                title[:position].strip()
            )

            if possible_brand:

                words = possible_brand.split()

                if len(words) <= 5:

                    return possible_brand

    return "Unknown"


# ==========================================
# NORMALIZE BRAND NAME
# ==========================================

def normalize_brand_name(brand_name):
    """
    Normalize a brand name for deduplication.
    """

    if not brand_name:

        return "unknown"

    return (
        brand_name
        .lower()
        .strip()
        .replace("  ", " ")
    )


# ==========================================
# REMOVE DUPLICATE LEADS
# ==========================================

def remove_duplicate_leads(leads):
    """
    Remove duplicate brands while keeping
    separate unknown leads.
    """

    unique_leads = {}

    for lead in leads:

        brand_name = lead.get(
            "brand_name",
            "Unknown"
        )

        normalized_name = (
            normalize_brand_name(
                brand_name
            )
        )

        if normalized_name == "unknown":

            normalized_name = (
                "unknown_"
                + str(
                    len(unique_leads) + 1
                )
            )

        if normalized_name not in unique_leads:

            unique_leads[
                normalized_name
            ] = lead

        else:

            unique_leads[
                normalized_name
            ]["source_count"] += 1

    return list(
        unique_leads.values()
    )


# ==========================================
# SAVE LEADS TO DATABASE
# ==========================================

def save_leads_to_database(leads):
    """
    Save discovered leads into PostgreSQL.
    """

    db = SessionLocal()

    saved_count = 0

    try:

        for lead in leads:

            save_lead(
                db,
                lead
            )

            saved_count += 1

    except Exception as e:

        db.rollback()

        print(
            "\nDatabase error:"
        )

        print(e)

    finally:

        db.close()

    return saved_count


# ==========================================
# RUN DISCOVERY
# ==========================================

def run_discovery():
    """
    Run the complete VEXA discovery pipeline.
    """

    print(
        "\n=========================================="
    )

    print(
        "VEXA AI DISCOVERY ENGINE"
    )

    print(
        "=========================================="
    )


    # ----------------------------------------
    # STEP 1: DISCOVER NEWS
    # ----------------------------------------

    print(
        "\n[1/5] Discovering news articles..."
    )

    query = (
        "India esports sponsorship brands"
    )

    results = discover_news(
        query,
        max_results=10
    )


    # ----------------------------------------
    # HANDLE DISCOVERY ERROR
    # ----------------------------------------

    if isinstance(results, dict):

        error_message = results.get(
            "error",
            "Unknown discovery error"
        )

        print(
            "\nDiscovery error:"
        )

        print(
            error_message
        )

        return {
            "status": "failed",
            "message": "News discovery failed.",
            "error": error_message,
            "articles_found": 0,
            "leads_found": 0,
            "leads_saved": 0
        }


    # ----------------------------------------
    # NO RESULTS
    # ----------------------------------------

    if not results:

        print(
            "\nNo news results were found."
        )

        return {
            "status": "completed",
            "message": "No news results were found.",
            "articles_found": 0,
            "leads_found": 0,
            "leads_saved": 0
        }


    print(
        f"Found {len(results)} articles."
    )


    # ----------------------------------------
    # STEP 2: PROCESS ARTICLES
    # ----------------------------------------

    print(
        "\n[2/5] Processing articles..."
    )

    leads = []


    for article in results:

        try:

            # Clean article
            clean_article = (
                clean_news_article(
                    article
                )
            )


            # Basic classification
            classification = (
                classify_lead(
                    clean_article
                )
            )


            # Extract brand
            brand_name = (
                extract_brand_name(
                    clean_article
                )
            )


            # Create initial lead
            lead = {

                "brand_name": brand_name,

                "lead_type": classification[
                    "lead_type"
                ],

                "priority": classification[
                    "priority"
                ],

                "gaming_signal": classification[
                    "gaming_signal"
                ],

                "sponsorship_signal": classification[
                    "sponsorship_signal"
                ],

                "title": clean_article[
                    "title"
                ],

                "published_at": clean_article[
                    "published_at"
                ],

                "description": clean_article[
                    "description"
                ],

                "source_url": clean_article[
                    "url"
                ],

                "source_count": 1
            }


            # --------------------------------
            # AI ANALYSIS
            # --------------------------------

            ai_result = analyze_brand(
                lead
            )


            lead["industry"] = (
                ai_result.get(
                    "industry",
                    "Unknown"
                )
            )

            lead["gaming_activity"] = (
                ai_result.get(
                    "gaming_activity",
                    ""
                )
            )

            lead["sponsorship_activity"] = (
                ai_result.get(
                    "sponsorship_activity",
                    ""
                )
            )

            lead["opportunity"] = (
                ai_result.get(
                    "opportunity",
                    ""
                )
            )

            lead["reasoning"] = (
                ai_result.get(
                    "reasoning",
                    ""
                )
            )


            # --------------------------------
            # OPPORTUNITY SCORING
            # --------------------------------

            score_result = analyze_lead(
                lead
            )


            lead["opportunity_score"] = (
                score_result.get(
                    "opportunity_score",
                    0
                )
            )

            lead["priority"] = (
                score_result.get(
                    "priority",
                    lead["priority"]
                )
            )


            leads.append(
                lead
            )


        except Exception as error:

            print(
                f"Failed to process article: {error}"
            )


    print(
        f"Processed {len(leads)} potential leads."
    )


    # ----------------------------------------
    # STEP 3: REMOVE DUPLICATES
    # ----------------------------------------

    print(
        "\n[3/5] Removing duplicate leads..."
    )

    unique_leads = (
        remove_duplicate_leads(
            leads
        )
    )


    print(
        f"{len(unique_leads)} unique leads remain."
    )


    # ----------------------------------------
    # STEP 4: SAVE TO DATABASE
    # ----------------------------------------

    print(
        "\n[4/5] Saving leads to PostgreSQL..."
    )

    saved_count = (
        save_leads_to_database(
            unique_leads
        )
    )


    print(
        f"Saved {saved_count} leads."
    )


    # ----------------------------------------
    # STEP 5: COMPLETE
    # ----------------------------------------

    print(
        "\n[5/5] Discovery completed."
    )


    return {

        "status": "completed",

        "message": (
            "Discovery completed successfully."
        ),

        "articles_found": len(
            results
        ),

        "leads_found": len(
            unique_leads
        ),

        "leads_saved": saved_count
    }


# ==========================================
# DIRECT SCRIPT EXECUTION
# ==========================================

if __name__ == "__main__":

    result = run_discovery()

    print(
        "\n=========================================="
    )

    print(
        "FINAL RESULT"
    )

    print(
        "=========================================="
    )

    print(
        result
    )