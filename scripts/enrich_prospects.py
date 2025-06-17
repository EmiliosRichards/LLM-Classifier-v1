import csv
import os
import json
import sys
import requests
from bs4 import BeautifulSoup
from google import generativeai as genai
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classifier import classify_blurb

load_dotenv()

# Task 3.2: Implement Placeholder Scraper
def scrape_url(url):
    """
    Scrapes a URL, extracts the text content, and returns it.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the body tag and get all the text
        body = soup.find('body')
        if body:
            return body.get_text(separator=' ', strip=True)
        return ""  # Return empty string if no body tag is found
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return ""

# Task 3.3: Implement Two-Step LLM Pipeline (Summarizer)
def get_summary(full_text):
    """
    Uses the live Gemini API to generate a summary of a company's main products and customer segments.
    """
    prompt_template = (
        "As a business analyst, return a concise, 2-3 sentence summary of a company's "
        "main products and primary customer segments based on the text provided."
    )

    try:
        # Configure the genai client using the API key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Use the gemini-2.0-flash model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Call the generate_content method with the prompt and the full text
        prompt = f"{prompt_template}\n\nTEXT: {full_text}"
        response = model.generate_content(prompt)
        
        # Return the response.text on success
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return ""

# Tasks 3.4 & 3.5: Implement Main Processing Logic
def main():
    """
    Main function to orchestrate the prospect enrichment pipeline.
    """
    # Prepare output and log directories
    os.makedirs('output', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Define file paths
    input_file = 'data/Manuav B-Liste Export.csv'
    output_file = 'output/prospects_with_codes.csv'
    log_file = 'logs/unknown_log.csv'

    # Define headers
    output_headers = ['firma', 'url', 'audience_codes']
    log_headers = ['firma', 'url', 'summary']

    print(f"Starting prospect enrichment process...")
    print(f"Input file: {input_file}")

    with open(input_file, mode='r', encoding='latin-1') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile, \
         open(log_file, mode='w', newline='', encoding='utf-8') as logfile:

        reader = csv.DictReader(infile)
        
        output_writer = csv.DictWriter(outfile, fieldnames=output_headers)
        output_writer.writeheader()
        
        log_writer = csv.DictWriter(logfile, fieldnames=log_headers)
        log_writer.writeheader()

        for row in reader:
            firma = row.get('firma')
            url = row.get('url')

            if not url:
                continue

            # Task 3.3 Orchestration
            # 1. Scrape URL to get fake full text
            full_text = scrape_url(url)
            
            # 2. Get clean summary
            summary = get_summary(full_text)
            
            # 3. Classify the summary to get codes
            audience_codes = classify_blurb(summary)

            # Logging for UNKNOWN/OTHER
            primary_code = audience_codes.get('primary')
            if primary_code in ['UNKNOWN', 'OTHER']:
                log_writer.writerow({
                    'firma': firma,
                    'url': url,
                    'summary': summary
                })

            # Write to main output file
            output_writer.writerow({
                'firma': firma,
                'url': url,
                'audience_codes': json.dumps(audience_codes)
            })

    print(f"Processing complete.")
    print(f"Results saved to: {output_file}")
    print(f"Log for 'UNKNOWN' or 'OTHER' classifications saved to: {log_file}")

# Add Execution Block
if __name__ == "__main__":
    main()