import csv
import os
import json

# Task 4.2: Implement Scoring Logic
# --- Constants for scoring weights ---
VERTICAL_WEIGHT = 1.0
HORIZONTAL_WEIGHT = 0.5
FUNCTIONAL_WEIGHT = 0.8
SPECIAL_VERTICAL_WEIGHT = 1.2 # e.g., for regulated industries
SPECIAL_FUNCTIONAL_WEIGHT = 1.1 # e.g., for critical functions

# --- Score Boosts ---
EVALUATION_SCORE_BOOST = 0.1 # 10% boost for each point of evaluation score
LEAD_VOLUME_BOOST = 0.05 # 5% boost for high lead volume partners

# --- Code Sets ---
# Using sets for efficient lookups
SPECIAL_SET = {'X_HORIZ', 'X_SME', 'F_HR', 'F_SALES', 'F_OPS'}
REGULATED_SET = {'FIN_BANK', 'FIN_INS', 'HC_HOSP', 'HC_PHARM'}

def calculate_match_score(prospect_codes, partner_codes, partner_row):
    """
    Calculates the match score between a prospect and a partner based on their audience codes.

    Args:
        prospect_codes (list): A list of audience codes for the prospect.
        partner_codes (list): A list of audience codes for the partner.
        partner_row (dict): The full data row for the partner, used for boosts.

    Returns:
        tuple: A tuple containing the final score (float) and the type of overlap (str).
               Returns (0, 'No Overlap') if there's no match.
    """
    prospect_set = set(prospect_codes)
    partner_set = set(partner_codes)

    # Find the intersection of codes
    overlap = prospect_set.intersection(partner_set)

    if not overlap:
        return 0, "No Overlap"

    base_score = 0
    overlap_type = "Unknown"

    # Determine the highest-value match type based on weights
    # This logic prioritizes the highest value match if multiple exist
    is_vertical = any(code.startswith('V_') for code in overlap)
    is_functional = any(code.startswith('F_') for code in overlap)
    is_horizontal = any(code.startswith('X_') for code in overlap)
    is_regulated = any(code in REGULATED_SET for code in overlap)

    if is_vertical:
        base_score = SPECIAL_VERTICAL_WEIGHT if is_regulated else VERTICAL_WEIGHT
        overlap_type = 'VERTICAL'
    elif is_functional:
        base_score = FUNCTIONAL_WEIGHT
        overlap_type = 'FUNCTIONAL'
    elif is_horizontal:
        base_score = HORIZONTAL_WEIGHT
        overlap_type = 'HORIZONTAL'

    # --- Apply Score Boosts ---
    final_score = base_score

    # Boost based on partner's Evaluation Score
    try:
        eval_score = float(partner_row.get('Evaluation Score', 0))
        if eval_score > 0:
            final_score *= (1 + (eval_score * EVALUATION_SCORE_BOOST))
    except (ValueError, TypeError):
        pass # Ignore if the score is not a valid number

    # Boost based on Average Leads Per Day
    try:
        avg_leads = float(partner_row.get('Avg Leads Per Day', 0))
        if avg_leads > 50: # Example threshold for a high-volume partner
            final_score *= (1 + LEAD_VOLUME_BOOST)
    except (ValueError, TypeError):
        pass # Ignore if leads are not a valid number

    return final_score, overlap_type

# Task 4.3 & 4.4: Main Processing Logic and Report Generation
def main():
    """
    Main function to load data, run the matching process, and generate the final report.
    """
    print("Starting matching process...")

    # Define file paths
    partners_file = os.path.join('output', 'partners_with_codes.csv')
    prospects_file = os.path.join('output', 'prospects_with_codes.csv')
    output_file = os.path.join('output', 'matches_v1.csv')

    # Load data
    try:
        with open(partners_file, mode='r', encoding='utf-8') as infile:
            partners = list(csv.DictReader(infile))
        with open(prospects_file, mode='r', encoding='utf-8') as infile:
            prospects = list(csv.DictReader(infile))
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the input files exist.")
        return

    all_results = []

    print(f"Comparing {len(prospects)} prospects against {len(partners)} partners...")

    # Run Match: Nested loop to compare every prospect against every partner
    for prospect in prospects:
        prospect_id = prospect.get('firma', 'Unknown Prospect')
        try:
            # Safely load JSON string from the CSV
            # Safely load JSON string and extract codes
            prospect_data = json.loads(prospect.get('audience_codes', '{}'))
            prospect_codes = []
            if isinstance(prospect_data, dict):
                if prospect_data.get('primary'):
                    prospect_codes.append(prospect_data['primary'])
                if prospect_data.get('secondary'):
                    prospect_codes.extend(prospect_data['secondary'])
        except (json.JSONDecodeError, TypeError):
            prospect_codes = [] # Default to empty list on error

        for partner in partners:
            partner_id = partner.get('Company Name', 'Unknown Partner')
            try:
                # Safely load JSON string and extract codes
                partner_data = json.loads(partner.get('audience_codes', '{}'))
                partner_codes = []
                if isinstance(partner_data, dict):
                    if partner_data.get('primary'):
                        partner_codes.append(partner_data['primary'])
                    if partner_data.get('secondary'):
                        partner_codes.extend(partner_data['secondary'])
            except (json.JSONDecodeError, TypeError):
                partner_codes = [] # Default to empty list on error

            score, overlap_type = calculate_match_score(prospect_codes, partner_codes, partner)

            if score > 0:
                all_results.append({
                    'prospect_firma': prospect_id,
                    'prospect_url': prospect.get('url', ''),
                    'partner_name': partner_id,
                    'partner_evaluation_score': partner.get('Evaluation Score', ''),
                    'partner_avg_leads': partner.get('Avg Leads Per Day', ''),
                    'match_score': score,
                    'overlap_type': overlap_type
                })

    print(f"Found {len(all_results)} potential matches. Generating report...")

    # Generate Report: Find top 5 partners for each prospect
    final_report_data = []
    prospects_processed = {} # To store top matches for each prospect

    # Group results by prospect
    for result in all_results:
        prospect_name = result['prospect_firma']
        if prospect_name not in prospects_processed:
            prospects_processed[prospect_name] = []
        prospects_processed[prospect_name].append(result)

    # Sort and get top 5 for each prospect
    for prospect_name, matches in prospects_processed.items():
        # Sort matches by score in descending order
        sorted_matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)
        # Add the top 5 to the final report list
        final_report_data.extend(sorted_matches[:5])


    # Write the final report
    if final_report_data:
        headers = [
            'prospect_firma', 'prospect_url', 'partner_name',
            'partner_evaluation_score', 'partner_avg_leads',
            'match_score', 'overlap_type'
        ]
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(final_report_data)
        print(f"Successfully generated report at {output_file}")
    else:
        print("No matches found to generate a report.")

# Execution Block
if __name__ == "__main__":
    main()