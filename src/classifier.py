import json
import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()

# Define the cache file path
CACHE_FILE = 'cache.json'

# Sub-Tasks 1.3.2 & 1.3.3: Design and Populate LLM Prompt
PROMPT_TEMPLATE = """
You are a highly intelligent text classification engine. Your task is to analyze the provided company description and classify it into the most relevant primary and secondary categories based on the given taxonomy.

**Classification Rules:**
1.  **Primary Category:** You must choose exactly one primary category from the provided taxonomy. This should be the most fitting category that describes the company's core business.
2.  **Secondary Categories:** You may choose one or more secondary categories that also describe the company's business, but are less central than the primary category. If no secondary categories apply, return an empty list.
3.  **JSON Output:** Your final output must be a single, valid JSON object with three keys:
    *   `"primary"`: A string representing the single primary category code.
    *   `"secondary"`: A list of strings representing the secondary category codes.
    *   `"explanation"`: A brief (1-2 sentence) explanation for your choices.

**Taxonomy:**
```json
{{taxonomy}}
```

**Company Description:**
"{{description}}"

**Examples:**

*   **Description:** "We are a leading provider of cloud-based human resources software, helping businesses manage payroll, benefits, and talent acquisition."
    *   **Expected Output:**
        ```json
        {
          "primary": "F_HR",
          "secondary": ["S_SW"],
          "explanation": "The company's core business is HR software, which falls under the 'Functional > Human Resources' category. As it is a software provider, 'Sector > Software' is a fitting secondary category."
        }
        ```
*   **Description:** "Our firm offers strategic consulting services to help enterprises navigate digital transformation, improve operational efficiency, and drive growth."
    *   **Expected Output:**
        ```json
        {
          "primary": "X_HORIZ",
          "secondary": ["S_CS"],
          "explanation": "The company provides broad, cross-functional consulting services, which aligns with the 'Cross-Functional > Horizontal' category. 'Sector > Consulting Services' is an appropriate secondary classification."
        }
        ```
*   **Description:** "We manufacture high-precision components for the aerospace and defense industries, specializing in CNC machining and composite materials."
    *   **Expected Output:**
        ```json
        {
          "primary": "X_SME",
          "secondary": ["S_MFG"],
          "explanation": "The company operates as a specialized small-to-medium enterprise (SME) within a niche manufacturing sector. 'Sector > Manufacturing' is a relevant secondary category."
        }
        ```

Now, based on the provided taxonomy and company description, please classify the company.
"""

# Sub-Task 1.3.1: Implement load_taxonomy()
def load_taxonomy():
    """
    Reads the taxonomy file and returns it as a dictionary.
    """
    try:
        with open('audience_taxonomy_v2025-06.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Taxonomy file not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the taxonomy file.")
        return {}

# Sub-Task 1.3.5: Implement Caching
def load_cache():
    """
    Loads the cache from cache.json.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache_data):
    """
    Saves the cache data to cache.json.
    """
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f, indent=4)

# Sub-Task 1.3.4: Implement build_prompt()
def build_prompt(description, taxonomy_codes):
    """
    Formats the PROMPT_TEMPLATE with the company description and taxonomy.
    """
    taxonomy_str = json.dumps(taxonomy_codes, indent=2)
    prompt = PROMPT_TEMPLATE.replace('{{taxonomy}}', taxonomy_str)
    prompt = prompt.replace('{{description}}', description)
    return prompt

# Sub-Task 1.3.6: Implement call_llm()
def call_llm(prompt):
    """
    Sends the prompt to the Gemini API and returns the response.
    """
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"temperature": 0.0},
        )

        response = model.generate_content(prompt)
        # Log the raw response for debugging
        print("----------- RAW LLM RESPONSE -----------")
        print(response.text)
        print("------------------------------------")
        return response.text
    except Exception as e:
        print(f"An error occurred during the Gemini API call: {e}")
        return json.dumps({"error": f"Gemini API call failed: {str(e)}"})

# Sub-Task 1.3.7: Implement classify_blurb()
def classify_blurb(description):
    """
    Main orchestrator function to classify a company description.
    """
    # a. Load the taxonomy
    taxonomy = load_taxonomy()
    if not taxonomy:
        return {"error": "Failed to load taxonomy."}

    # b. Load the cache
    cache = load_cache()

    # c. Check if the description is in the cache
    if description in cache:
        print("--- CACHE HIT ---")
        return cache[description]

    print("--- CACHE MISS ---")
    # d. If not in cache, build the prompt
    prompt = build_prompt(description, taxonomy)

    # e. Call the LLM
    llm_response_str = call_llm(prompt)

    # f. Parse the JSON response
    try:
        # Clean the response string by removing markdown backticks and "json" identifier
        clean_response = llm_response_str.strip().replace('```json', '').replace('```', '').strip()
        result = json.loads(clean_response)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from response: {llm_response_str}")
        return {"error": "Failed to parse LLM response."}

    # g. Update the cache and save it
    cache[description] = result
    save_cache(cache)

    # h. Return the parsed JSON result
    return result

if __name__ == '__main__':
    # Example usage:
    test_description = "A sample company that provides horizontal business solutions for SMEs."
    classification = classify_blurb(test_description)
    print("\nClassification Result:")
    print(json.dumps(classification, indent=2))

    # Second call to test caching
    print("\n--- Making a second call for the same description to test caching ---")
    classification_cached = classify_blurb(test_description)
    print("\nCached Classification Result:")
    print(json.dumps(classification_cached, indent=2))