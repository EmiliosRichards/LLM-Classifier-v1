# Definitive Project Plan (v5)

This document outlines the final, most granular plan for the project. It integrates the LLM-based partner classification strategy while preserving all detailed sub-tasks and adding difficulty scores. This is the single source of truth for the project.

---
### **Phase 1: Core Classifier Development & Testing**
*Goal: Build and validate the single, unified LLM classifier that will be used for both partners and prospects.*

*   **Task 1.1: Finalize Taxonomy File** (Difficulty: 1/10)
*   **Task 1.2: Create Classifier Script** (Difficulty: 2/10)
*   **Task 1.3: Implement Core Classifier Functions** (Overall Difficulty: 7/10)
    *   **Sub-Task 1.3.1:** Implement `load_taxonomy()` to read and parse the JSON file. (Difficulty: 2/10)
    *   **Sub-Task 1.3.2:** Design the LLM prompt template as a multi-line string. (Difficulty: 3/10)
    *   **Sub-Task 1.3.3:** Populate the template with classification rules and the three few-shot examples. (Difficulty: 4/10)
    *   **Sub-Task 1.3.4:** Implement `build_prompt()` to inject data into the template. (Difficulty: 2/10)
    *   **Sub-Task 1.3.5:** Implement a file-based caching mechanism. (Difficulty: 4/10)
    *   **Sub-Task 1.3.6:** Implement `call_llm()` to handle the external API call. (Difficulty: 3/10)
    *   **Sub-Task 1.3.7:** Implement the main `classify_blurb()` orchestrator function. (Difficulty: 3/10)
*   **Task 1.4: Create a Dedicated Test Script** (Difficulty: 3/10)
*   **Task 1.5: Run Smoke Tests** (Overall Difficulty: 5/10)
    *   **Sub-Task 1.5.1:** Define a list of test cases with expected outputs. (Difficulty: 3/10)
    *   **Sub-Task 1.5.2:** Write a loop to run through the test cases. (Difficulty: 2/10)
    *   **Sub-Task 1.5.3:** Use `assert` statements to validate the results. (Difficulty: 2/10)
    *   **Sub-Task 1.5.4:** Run the test script and iterate on the prompt if necessary. (Difficulty: 4/10)

---
### **Phase 2: Partner Processing & Classification**
*Goal: Use the validated classifier to label the partner data.*

*   **Task 2.1: Create Partner Processing Script** (Difficulty: 2/10)
*   **Task 2.2: Implement Partner Data-to-Blurb Logic** (Overall Difficulty: 4/10)
    *   **Sub-Task 2.2.1:** In the script, read the partner CSV file.
    *   **Sub-Task 2.2.2:** Define a function `create_partner_blurb(row)` that takes a CSV row as input.
    *   **Sub-Task 2.2.3:** Inside the function, select the key columns (`Company Name`, `Industry`, `Products/Services Offered`, `USP`, etc.) and concatenate them into a single formatted, descriptive string.
*   **Task 2.3: Classify Partners & Generate Coded File** (Overall Difficulty: 4/10)
    *   **Sub-Task 2.3.1:** Loop through each partner row in the script.
    *   **Sub-Task 2.3.2:** Call `create_partner_blurb()` for the row.
    *   **Sub-Task 2.3.3:** Call the `classify_blurb()` function from the Phase 1 script with the generated blurb.
    *   **Sub-Task 2.3.4:** Save the results to `output/partners_with_codes.csv`.
*   **Task 2.4: Review and Spot-Check** (Difficulty: 1/10)

---
### **Phase 3: Prospect Enrichment & Classification**
*Goal: Use the same classifier to label the prospect data.*

*   **Task 3.1: Create Prospect Enrichment Script** (Difficulty: 2/10)
*   **Task 3.2: Process Prospects and Classify** (Overall Difficulty: 4/10)
    *   **Sub-Task 3.2.1:** In the script, load the prospect CSV file.
    *   **Sub-Task 3.2.2:** Loop through each row and call the `classify_blurb()` function using the `Beschreibung` column as input, storing the results.
*   **Task 3.3: Generate Coded Prospect File** (Difficulty: 3/10)
*   **Task 3.4: Implement Logging for Unknowns** (Difficulty: 2/10)

---
### **Phase 4: Matching, Scoring & Final Analysis**
*Goal: Run the final matching algorithm and generate the v1 report.*

*   **Task 4.1: Create Matching Script** (Difficulty: 2/10)
*   **Task 4.2: Implement Scoring Logic** (Overall Difficulty: 8/10)
    *   **Sub-Task 4.2.1:** Define scoring weight constants. (Difficulty: 2/10)
    *   **Sub-Task 4.2.2:** Define `SPECIAL` and `REGULATED_SET` collections. (Difficulty: 2/10)
    *   **Sub-Task 4.2.3:** Implement the base score logic for `overlap_type`. (Difficulty: 5/10)
    *   **Sub-Task 4.2.4:** Add logic for score boosts. (Difficulty: 3/10)
    *   **Sub-Task 4.2.5:** Handle zero-overlap cases. (Difficulty: 2/10)
*   **Task 4.3: Run the Full Match** (Overall Difficulty: 4/10)
    *   **Sub-Task 4.3.1:** Load the coded partner and prospect files.
    *   **Sub-Task 4.3.2:** Implement the nested loop for prospect-partner pairs.
    *   **Sub-Task 4.3.3:** Call the scoring function and store all results.
*   **Task 4.4: Generate Final Report** (Difficulty: 3/10)

---
### **Phase 5: Maintenance & Tuning**
*Goal: Establish a long-term process for improving the system's accuracy and relevance.*

*   **Task 5.1: Establish Weekly Log Review** (Difficulty: 2/10)
*   **Task 5.2: Institute Score Tuning Loop** (Overall Difficulty: 6/10)
    *   **Sub-Task 5.2.1:** Manually review the final `matches_v1.csv`. (Difficulty: 2/10)
    *   **Sub-Task 5.2.2:** Formulate a hypothesis for improvement. (Difficulty: 3/10)
    *   **Sub-Task 5.2.3:** Adjust weighting constants in the script. (Difficulty: 1/10)
    *   **Sub-Task 5.2.4:** Re-run the matching script and compare outputs to validate changes. (Difficulty: 3/10)