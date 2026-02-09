import anthropic
import json
from datetime import datetime
import os

# Get API key safely
api_key = os.environ.get(
    "ANTHROPIC_API_KEY") or "api-key-here"


def score_lead(inquiry_text):
    """
    Scores a customer inquiry on a 1-10 scale.

    Scoring criteria:
    1-3: Not a lead (spam, irrelevant, no budget)
    4-6: Maybe interested (curious, uncertain fit)
    7-10: Hot lead (ready to buy, clear need, has budget)

    Args:
        inquiry_text (str): Customer inquiry text

    Returns:
        dict: Contains score, reasoning, priority, and recommendation
    """

    client = anthropic.Anthropic(api_key=api_key)

    # The prompt is crucial - be very specific about scoring
    prompt = f"""You are a sales expert who evaluates leads.

Score this inquiry on a 1-10 scale based on:
1. Budget/ability to pay (do they mention budget or authority?)
2. Urgency (when do they need this?)
3. Problem fit (is this a real problem they have?)
4. Company size/legitimacy (are they a real prospect?)

Scale:
1-3 = Not a lead (spam, no real interest, no budget)
4-6 = Maybe interested (curious, uncertain fit, timing unclear)
7-10 = Hot lead (clear need, urgency, budget indication, decision maker)

Inquiry:
{inquiry_text}

Return ONLY valid JSON with NO markdown formatting:
{{
    "score": <1-10>,
    "reasoning": "<2-3 sentences explaining the score>",
    "priority": "<HIGH/MEDIUM/LOW>",
    "key_signals": ["signal1", "signal2", "signal3"],
    "recommendation": "<What should sales do next?>",
    "hot_buttons": ["if", "any", "urgent", "factors"],
    "concerns": ["if", "any", "concerning", "factors"]
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=400,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text.strip()

        # Clean up markdown if present
        if "```json" in response_text:
            response_text = response_text.split(
                "```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split(
                "```")[1].split("```")[0].strip()

        # Parse JSON
        result = json.loads(response_text)
        result["status"] = "success"
        result["original_inquiry"] = inquiry_text[:150] + \
            "..." if len(inquiry_text) > 150 else inquiry_text
        result["timestamp"] = datetime.now().isoformat()

        return result

    except json.JSONDecodeError as e:
        return {
            "score": None,
            "status": "failed",
            "error": f"JSON parsing error: {str(e)}",
            "raw_response": response_text if 'response_text' in locals() else "No response"
        }

    except Exception as e:
        return {
            "score": None,
            "status": "failed",
            "error": str(e),
            "original_inquiry": inquiry_text[:150] + "..."
        }


def score_multiple_leads(inquiry_list):
    """
    Score multiple leads and sort by priority.

    Args:
        inquiry_list (list): List of inquiry text strings

    Returns:
        dict: Sorted results with analytics
    """

    results = []

    print(f"Scoring {len(inquiry_list)} leads...\n")

    for i, inquiry in enumerate(inquiry_list, 1):
        print(f"Lead {i}/{len(inquiry_list)}...", end=" ")
        result = score_lead(inquiry)
        results.append(result)
        print("✓")

    # Sort by score (highest first)
    successful_leads = [r for r in results if r.get("status") == "success"]
    successful_leads.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Analytics
    analytics = {
        "total_leads": len(results),
        "scored_successfully": len(successful_leads),
        "hot_leads_count": len([r for r in successful_leads if r.get("score", 0) >= 7]),
        "warm_leads_count": len([r for r in successful_leads if 4 <= r.get("score", 0) < 7]),
        "cold_leads_count": len([r for r in successful_leads if r.get("score", 0) < 4]),
        "average_score": sum(r.get("score", 0) for r in successful_leads) / len(successful_leads) if successful_leads else 0
    }

    return {
        "all_results": results,
        "sorted_by_priority": successful_leads,
        "analytics": analytics
    }


def save_lead_scores(scoring_results, filename=None):
    """
    Save lead scoring results to JSON file.

    Args:
        scoring_results (dict): Results from score_multiple_leads
        filename (str): Optional custom filename

    Returns:
        str: Filename saved
    """

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lead_scores_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(scoring_results, f, indent=2)

    print(f"\n✓ Results saved to: {filename}")
    return filename


def print_lead_summary(scoring_results):
    """
    Print a nice summary of lead scoring results.
    """

    analytics = scoring_results["analytics"]
    sorted_leads = scoring_results["sorted_by_priority"]

    print("\n" + "=" * 70)
    print("LEAD SCORING SUMMARY")
    print("=" * 70)

    print(f"\n📊 ANALYTICS:")
    print(f"   Total leads scored: {analytics['total_leads']}")
    print(f"   Successfully scored: {analytics['scored_successfully']}")
    print(f"   Average score: {analytics['average_score']:.1f}/10")
    print(f"\n   🔥 Hot leads (7-10): {analytics['hot_leads_count']}")
    print(f"   🟡 Warm leads (4-6): {analytics['warm_leads_count']}")
    print(f"   ❄️  Cold leads (1-3): {analytics['cold_leads_count']}")

    print(f"\n📌 TOP 5 LEADS (by score):")
    print("-" * 70)

    for i, lead in enumerate(sorted_leads[:5], 1):
        if lead.get("status") == "success":
            score = lead.get("score", "?")
            priority = lead.get("priority", "?")
            reasoning = lead.get("reasoning", "No reasoning")

            print(f"\n{i}. Score: {score}/10 [{priority}]")
            print(f"   Reasoning: {reasoning}")
            print(f"   Recommendation: {lead.get('recommendation', 'N/A')}")


# ============================================================================
# TESTING - RUN THIS SECTION FIRST
# ============================================================================

if __name__ == "__main__":

    # Test with sample leads
    test_leads = [
        """
Hi there,

We're a Fortune 500 company with 5,000 employees. We've been looking to implement 
AI automation for 6 months. Budget has been approved ($50k). We need to start 
implementation within 2 weeks for Q1 targets.

When can we schedule a demo?

Thanks,
John Smith
VP Operations
TechCorp Inc.
        """,

        """
just browsing your site, looks cool
        """,

        """
Hello,

Small team here (10 people). We're interested in what you do but not sure if 
we're a fit. Budget is tight this quarter. Might revisit next year.

Just wanted to learn more.

Thanks,
Sarah
        """,

        """
We're in crisis mode. Our current system is down and we need an emergency solution TODAY. 
We'll authorize any cost necessary. This is urgent - can you help immediately?

Let me know ASAP.

Regards,
Mike
CEO
        """,

        """
Your product looks interesting. We're a startup with limited budget but we're growing fast.
We might need this in 6 months if things go well. 

Let me know more details.

Best,
Alex
        """,

        """
CLICK HERE FOR FREE MONEY!!!
LIMITED TIME OFFER!!!
        """
    ]

    print("=" * 70)
    print("LEAD QUALITY SCORER - TEST RUN")
    print("=" * 70)

    # Score all leads
    results = score_multiple_leads(test_leads)

    # Print summary
    print_lead_summary(results)

    # Save results
    save_lead_scores(results)

    # Show top lead details
    if results["sorted_by_priority"]:
        print(f"\n" + "=" * 70)
        print("TOP LEAD DETAILS:")
        print("=" * 70)

        top_lead = results["sorted_by_priority"][0]

        print(f"\n🎯 HOTTEST LEAD")
        print(f"Score: {top_lead.get('score')}/10")
        print(f"Priority: {top_lead.get('priority')}")
        print(f"\nKey Signals: {', '.join(top_lead.get('key_signals', []))}")
        print(f"\nReasoning: {top_lead.get('reasoning')}")
        print(f"\nNext Steps: {top_lead.get('recommendation')}")
