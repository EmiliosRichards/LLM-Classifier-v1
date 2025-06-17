import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.enrich_prospects import scrape_url, get_summary
from src.classifier import classify_blurb

def test_prospect_pipeline():
    """
    Tests the full, live prospect enrichment pipeline on a single, real-world example.
    """
    # A known, stable URL for a company with a clear purpose.
    test_url = "https://www.atlassian.com/software/jira"

    print(f"--- Testing pipeline for URL: {test_url} ---")

    # 1. Scrape the URL
    print("Step 1: Scraping URL...")
    full_text = scrape_url(test_url)
    assert full_text is not None and len(full_text) > 100, "Scraping failed or returned too little content."
    print("Scraping successful.")

    # 2. Summarize the text
    print("Step 2: Summarizing content...")
    summary = get_summary(full_text)
    assert summary is not None and len(summary) > 10, "Summarization failed or returned an empty summary."
    print(f"Summary received: {summary}")

    # 3. Classify the summary
    print("Step 3: Classifying summary...")
    result = classify_blurb(summary)
    print(f"Classification result: {result}")

    # 4. Assert the result structure
    assert isinstance(result, dict), "Classification result is not a dictionary."
    assert 'primary' in result, "Result dictionary is missing 'primary' key."
    assert 'secondary' in result, "Result dictionary is missing 'secondary' key."
    assert 'explanation' in result, "Result dictionary is missing 'explanation' key."
    assert isinstance(result['primary'], str)
    assert isinstance(result['secondary'], list)
    assert isinstance(result['explanation'], str)

    print("--- Pipeline test passed successfully! ---")

if __name__ == "__main__":
    test_prospect_pipeline()