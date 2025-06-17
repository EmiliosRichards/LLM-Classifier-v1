import csv
import os
import json
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classifier import classify_blurb

def create_partner_blurb(row):
    """
    Creates a descriptive paragraph from a CSV row.
    """
    return (
        f"{row['Company Name']} is a company in the {row['Industry']} sector. "
        f"They offer {row['Products/Services Offered']}. "
        f"Their unique selling proposition is: {row['USP (Unique Selling Proposition) / Key Selling Points']}"
    )

def main():
    """
    Main function to process the partner data.
    """
    input_file = 'data/kgs_001_ER47_20250617.csv'
    output_dir = 'output'
    output_file = os.path.join(output_dir, 'partners_with_codes.csv')

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_headers = ['Company Name', 'Evaluation Score', 'Avg Leads Per Day', 'audience_codes']

    with open(input_file, mode='r', encoding='latin-1') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=output_headers)
        writer.writeheader()

        for row in reader:
            description = create_partner_blurb(row)
            audience_codes = classify_blurb(description)
            
            output_row = {
                'Company Name': row['Company Name'],
                'Evaluation Score': row['Evaluation Score'],
                'Avg Leads Per Day': row['Avg Leads Per Day'],
                'audience_codes': json.dumps(audience_codes)
            }
            writer.writerow(output_row)

    print(f"Processing complete. Output written to {output_file}")

if __name__ == "__main__":
    main()