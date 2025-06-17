# Definitive Project Plan (v6) - Verbose Edition

This document provides a comprehensive, detailed breakdown of the project plan. Each task and sub-task includes an explanation of the "What, Why, and How" to ensure clarity for all stakeholders, regardless of their prior context on the project. This is the final version, incorporating all refinements.

---
## **Phase 1: Core Classifier Development & Testing**
*Goal: Build and validate the single, unified LLM classifier that will be used for both partners and prospects.*

*   **Task 1.1: Finalize Taxonomy File** (Difficulty: 1/10)
    *   **What:** Add the `F_SALES` and `F_OPS` codes to the `audience_taxonomy_v2025-06.json` file.
    *   **Why:** To ensure our classification system covers all relevant business functions before we start using it to label data. This prevents rework and ensures the taxonomy is complete for the initial version.
    *   **How:** By manually editing the JSON file to insert two new key-value pairs into the list of codes.

*   **Task 1.2: Create Classifier Script** (Difficulty: 2/10)
    *   **What:** Create a new, empty Python file at `src/classifier.py`.
    *   **Why:** To establish a dedicated, central location for all code related to the core AI classification logic, keeping the project organized.
    *   **How:** By creating a new file within the `src` directory.

*   **Task 1.3: Implement Core Classifier Functions** (Overall Difficulty: 7/10)
    *   **Sub-Task 1.3.1:** Implement `load_taxonomy()` (Difficulty: 2/10)
        *   **What:** Create a Python function that reads and parses the `audience_taxonomy_v2025-06.json` file.
        *   **Why:** To make the taxonomy data easily accessible as a Python dictionary within our scripts for use in prompts and validation.
        *   **How:** Using Python's built-in `json` library, specifically `json.load()`, inside a function that returns the dictionary.
    *   **Sub-Task 1.3.2:** Design the LLM prompt template (Difficulty: 3/10)
        *   **What:** Create a multi-line string in `src/classifier.py` that will serve as the template for our instructions to the AI.
        *   **Why:** A template standardizes the instructions we give the AI, ensuring consistent and predictable behavior. It separates the static rules from the dynamic data (like the company description).
        *   **How:** By defining a Python constant (e.g., `PROMPT_TEMPLATE`) containing the instructional text and placeholders for dynamic content.
    *   **Sub-Task 1.3.3:** Populate the template with rules and examples (Difficulty: 4/10)
        *   **What:** Write the specific text for the prompt, including the rules for classification and the three few-shot examples (`X_HORIZ`, `F_HR`, `X_SME`).
        *   **Why:** This is the "teaching" part of the prompt. Clear rules and concrete examples dramatically improve the AI's accuracy and help it understand nuanced cases.
        *   **How:** By carefully writing the instructional text and embedding it into the prompt template string.
    *   **Sub-Task 1.3.4:** Implement `build_prompt()` (Difficulty: 2/10)
        *   **What:** Create a function that takes a company description and the list of taxonomy codes and injects them into the prompt template.
        *   **Why:** To dynamically create a complete, ready-to-use prompt for each classification request.
        *   **How:** Using Python's string formatting methods (e.g., f-strings) to combine the template with the function's input parameters.
    *   **Sub-Task 1.3.5:** Implement a file-based caching mechanism (Difficulty: 4/10)
        *   **What:** Create a simple system that saves the AI's response for a given company description to a local file (e.g., `cache.json`). Before making a new API call, the system will check if a response for that exact description already exists in the cache.
        *   **Why:** To significantly reduce costs and increase speed by avoiding redundant API calls for identical inputs.
        *   **How:** By using a dictionary to store descriptions and their corresponding AI outputs, and saving this dictionary to a JSON file. The main function will read from and write to this file.
    *   **Sub-Task 1.3.6:** Implement `call_llm()` (Difficulty: 3/10)
        *   **What:** Create a function that handles the technical details of sending the prompt to the LLM API and receiving the response.
        *   **Why:** To abstract the complexity of the API interaction into a single, reusable function.
        *   **How:** By using an appropriate library (like `requests` or a dedicated AI SDK) to make an HTTP POST request to the AI model's endpoint, including setting parameters like `temperature=0`.
    *   **Sub-Task 1.3.7:** Implement the main `classify_blurb()` orchestrator function (Difficulty: 3/10)
        *   **What:** Create the main function that ties all the other functions together: it checks the cache, builds the prompt, calls the LLM (if necessary), and returns the final classification.
        *   **Why:** To provide a single, simple entry point for the entire classification process that other scripts can easily call.
        *   **How:** By calling the other functions (`check_cache`, `build_prompt`, `call_llm`, `update_cache`) in the correct logical sequence.

*   **Task 1.4: Create a Dedicated Test Script** (Difficulty: 3/10)
    *   **What:** Create a new file at `tests/test_classifier.py`.
    *   **Why:** To keep our testing code separate from our application code, which is a standard best practice for software development.
    *   **How:** By creating a new file in a `tests` directory and adding `import` statements to bring in the functions from `src/classifier.py`.

*   **Task 1.5: Run Smoke Tests** (Overall Difficulty: 5/10)
    *   **What:** A series of simple, targeted tests to confirm the classifier is behaving as expected.
    *   **Why:** To gain confidence that our core AI logic is sound before we use it to process hundreds of rows of real data.
    *   **How:** By executing the `tests/test_classifier.py` script. The sub-tasks below detail the implementation.
    *   **Sub-Task 1.5.1:** Define test cases (Difficulty: 3/10)
        *   **What:** Create a list of Python dictionaries, where each dictionary contains a sample company description and the classification code we expect the AI to return.
        *   **Why:** To have a clear, objective set of criteria for what "correct" looks like for our classifier.
        *   **How:** By creating a list variable in `tests/test_classifier.py`.
    *   **Sub-Task 1.5.2:** Write a test loop (Difficulty: 2/10)
        *   **What:** Write a `for` loop that iterates over the list of test cases.
        *   **Why:** To systematically run the classifier against every test case we've defined.
        *   **How:** Using a standard `for` loop in Python.
    *   **Sub-Task 1.5.3:** Use `assert` statements (Difficulty: 2/10)
        *   **What:** Inside the loop, compare the actual output from the classifier with the expected output from the test case. The `assert` statement will cause the test to fail if they don't match.
        *   **Why:** To automatically and programmatically verify the correctness of the classifier's output.
        *   **How:** By writing `assert classifier_output == test_case['expected_output']`.
    *   **Sub-Task 1.5.4:** Run and iterate (Difficulty: 4/10)
        *   **What:** Execute the test script. If any tests fail, adjust the prompt text (from Sub-Task 1.3.3) to be clearer or provide better examples, and re-run the tests.
        *   **Why:** This is the core feedback loop for prompt engineering. It allows us to empirically improve the AI's performance until it meets our quality bar.
        *   **How:** By running `python tests/test_classifier.py` from the command line and editing the prompt string in `src/classifier.py` based on the failures.

---
## **Phase 2: Partner Processing & Classification**
*Goal: Use the validated classifier to label the partner data.*

*   **Task 2.1: Create Partner Processing Script** (Difficulty: 2/10)
    *   **What:** Create a new file at `scripts/process_partners.py`.
    *   **Why:** To have a dedicated script for the one-time task of processing the raw partner data file.
    *   **How:** By creating a new file in the `scripts` directory.

*   **Task 2.2: Implement Partner Data-to-Blurb Logic** (Overall Difficulty: 4/10)
    *   **What:** Create a function that combines several data fields from a partner's CSV row into a single descriptive paragraph.
    *   **Why:** To create a rich, context-filled input for the LLM classifier, which will yield much more accurate results than using a single data column.
    *   **How:** The sub-tasks below detail the implementation.
    *   **Sub-Task 2.2.1:** Read the partner CSV (Difficulty: 2/10)
        *   **What:** Open and load the `data/kgs_001_ER47_20250617.csv` file.
        *   **Why:** To get access to the raw partner data.
        *   **How:** Using Python's built-in `csv` library (specifically `csv.DictReader`) to easily access columns by name.
    *   **Sub-Task 2.2.2:** Define `create_partner_blurb(row)` (Difficulty: 2/10)
        *   **What:** Create a Python function that accepts a single row (as a dictionary) from the CSV file as input.
        *   **Why:** To encapsulate the logic for creating the descriptive paragraph, making the main script cleaner.
        *   **How:** By defining a new function in the script.
    *   **Sub-Task 2.2.3:** Concatenate key columns (Difficulty: 3/10)
        *   **What:** Inside the function, pull the text from the key columns (`Company Name`, `Industry`, `Products/Services Offered`, etc.) and join them together into a single string.
        *   **Why:** This is the core of the task, creating the rich "blurb" for the AI.
        *   **How:** Using f-strings to format the text from the different columns into a readable paragraph, e.g., `f"{row['Company Name']} is a company in the {row['Industry']} sector..."`.

*   **Task 2.3: Classify Partners & Generate Coded File** (Overall Difficulty: 4/10)
    *   **What:** Loop through the partners, classify each one using the AI, and save the results.
    *   **Why:** To produce the final, clean, coded partner dataset that will be used in the matching phase.
    *   **How:** The sub-tasks below detail the implementation.
    *   **Sub-Task 2.3.1:** Loop through partner rows (Difficulty: 2/10)
        *   **What:** Write a `for` loop to iterate over each row of the loaded partner data.
        *   **Why:** To process every partner in the input file.
        *   **How:** Using a standard `for` loop.
    *   **Sub-Task 2.3.2:** Call `create_partner_blurb()` (Difficulty: 1/10)
        *   **What:** Inside the loop, call the function from Task 2.2 to generate the descriptive paragraph for the current partner.
        *   **Why:** To prepare the input for the classifier.
        *   **How:** By calling the function: `blurb = create_partner_blurb(row)`.
    *   **Sub-Task 2.3.3:** Call the `classify_blurb()` function (Difficulty: 2/10)
        *   **What:** Call the main classifier function (from `src/classifier.py`) with the newly generated blurb.
        *   **Why:** To get the AI-generated audience codes for the partner.
        *   **How:** By importing the function and calling it: `codes = classify_blurb(blurb)`.
    *   **Sub-Task 2.3.4:** Save the results (Difficulty: 3/10)
        *   **What:** Write the results—including the company name, the new codes, and the scoring data—to a new file at `output/partners_with_codes.csv`.
        *   **Why:** To create the final, clean input file for the matching phase.
        *   **How:** By opening a new CSV file for writing and appending the results for each partner as they are processed.

*   **Task 2.4: Review and Spot-Check** (Difficulty: 1/10)
    *   **What:** Manually open the final `output/partners_with_codes.csv` file and look at a few rows.
    *   **Why:** To perform a final human sanity check that the process worked correctly and the output looks reasonable.
    *   **How:** By opening the file in a spreadsheet program or text editor.

---
## **Phase 3: Prospect Enrichment & Classification (v2)**
*Goal: Scrape prospect websites and use a two-step LLM process to accurately classify them.*

*   **Task 3.1: Create Prospect Enrichment Script** (Difficulty: 2/10)
    *   **What:** Create a new, empty Python file at `scripts/enrich_prospects.py`.
    *   **Why:** To have a dedicated, organized script for the entire prospect processing pipeline.
    *   **How:** By creating a new file in the `scripts` directory.

*   **Task 3.2: Implement Placeholder Scraper Function** (Difficulty: 2/10)
    *   **What:** Create a placeholder function `scrape_url(url)` within the new script. For now, this function will not perform actual web scraping but will return a pre-written, static block of sample text that mimics the content of a real webpage.
    *   **Why:** This is a crucial step for parallel development. It allows us to build and test the entire, complex LLM processing pipeline (summarization and classification) without needing to wait for the final scraper functionality to be built. It decouples the two efforts.
    *   **How:** By defining a simple function: `def scrape_url(url): return "This is a long block of sample text about a company that sells innovative software to enterprise-scale hospitals..."`.

*   **Task 3.3: Implement Two-Step LLM Processing Pipeline** (Overall Difficulty: 8/10)
    *   **What:** Build the core logic that takes the (currently fake) scraped text, summarizes it, and then classifies that summary.
    *   **Why:** This two-step method is more accurate and reliable than asking an LLM to classify a full, noisy webpage in one step. The summarization step cleans the data and provides a perfect input for our specialized classifier.
    *   **How:** The sub-tasks below detail the implementation.
    *   **Sub-Task 3.3.1:** Implement Summarization LLM Call (Difficulty: 5/10)
        *   **What:** Create a new function, `get_summary(full_text)`. This function will contain a new, dedicated prompt template that instructs the LLM to act as a business analyst, read the provided text, and return a concise, 2-3 sentence summary of the company's main products and primary customer segments.
        *   **Why:** To create a dedicated AI agent whose only job is to distill large, noisy text into a clean, factual summary. This separation of concerns is key to the pipeline's accuracy.
        *   **How:** By defining a new prompt template string, creating a function to call the LLM with this prompt, and including its own caching mechanism to avoid re-summarizing the same webpage text.
    *   **Sub-Task 3.3.2:** Orchestrate the Full Pipeline (Difficulty: 4/10)
        *   **What:** In the main processing loop of the script, orchestrate the sequence of calls:
            1.  Call `scrape_url()` to get the full text.
            2.  Call `get_summary()` with the full text to get the clean summary.
            3.  Call the `classify_blurb()` function (from `src/classifier.py`) with the clean summary to get the final codes.
        *   **Why:** To connect all the pieces of the pipeline into a single, logical workflow for each prospect.
        *   **How:** By calling the three functions in sequence within the main `for` loop and passing the output of one as the input to the next.

*   **Task 3.4: Generate Coded Prospect File** (Difficulty: 3/10)
    *   **What:** Save the final classification results to `output/prospects_with_codes.csv`.
    *   **Why:** To create the final, clean prospect dataset that will be used as input for the matching and scoring phase (Phase 4).
    *   **How:** By writing the prospect's `firma`, `url`, and the final `audience_codes` (from the classification step) to a new CSV file inside the main loop.

*   **Task 3.5: Implement Logging for Unknowns** (Difficulty: 2/10)
    *   **What:** If the final classification step returns `UNKNOWN` or `OTHER`, append the prospect's name, URL, and the intermediate summary to `logs/unknown_log.csv`.
    *   **Why:** To create a powerful feedback loop. Logging the summary (not the full text) makes it much faster for a human to review why a classification failed, which is essential for improving the taxonomy over time.
    *   **How:** By adding an `if` statement inside the loop that checks the result of the classification and appends the relevant data to the log file.

---
## **Phase 4: Matching, Scoring & Final Analysis**
*Goal: Run the final matching algorithm and generate the v1 report.*

*   **Task 4.1: Create Matching Script** (Difficulty: 2/10)
    *   **What:** Create a new file at `scripts/run_matching.py`.
    *   **Why:** To have a dedicated script for the final, most important business logic of the project.
    *   **How:** By creating a new file in the `scripts` directory.

*   **Task 4.2: Implement Scoring Logic** (Overall Difficulty: 8/10)
    *   **What:** Create the `calculate_match_score()` function, which contains the core business logic for determining how well a prospect matches a partner.
    *   **Why:** This is the heart of the project. The quality of this logic directly determines the value of the final output.
    *   **How:** The sub-tasks below detail the implementation.
    *   **Sub-Task 4.2.1:** Define scoring weight constants (Difficulty: 2/10)
        *   **What:** At the top of the script, define constants for all the different weights (e.g., `VERTICAL_WEIGHT = 1.0`, `HORIZONTAL_WEIGHT = 0.5`).
        *   **Why:** To keep all the "magic numbers" in one easy-to-find place, which makes tuning and adjustments (in Phase 5) much simpler.
        *   **How:** By defining variables like `VERTICAL_WEIGHT = 1.0`.
    *   **Sub-Task 4.2.2:** Define `SPECIAL` and `REGULATED_SET` (Difficulty: 2/10)
        *   **What:** Create Python sets containing the lists of special codes (`X_*`, `F_*`) and regulated industry codes (`FIN_*`, `HC_*`, etc.).
        *   **Why:** These sets make the scoring logic cleaner and more efficient, allowing for easy checks like `if code in SPECIAL:`.
        *   **How:** By defining two set variables: `SPECIAL = {'X_HORIZ', 'F_HR', ...}` and `REGULATED_SET = {'FIN_BANK', 'HC_HOSP', ...}`.
    *   **Sub-Task 4.2.3:** Implement base score logic (Difficulty: 5/10)
        *   **What:** Write the code that compares the two lists of codes (from the partner and prospect) and determines the highest-value match type based on the predefined weights.
        *   **Why:** This is the core comparison logic that decides if a match is Vertical, Functional, Horizontal, etc.
        *   **How:** By using loops and conditional (`if/elif/else`) statements to check for overlaps between the code sets in a specific, prioritized order.
    *   **Sub-Task 4.2.4:** Add logic for score boosts (Difficulty: 3/10)
        *   **What:** After the base score is calculated, add additional logic to increase the score based on the partner's `Evaluation Score` and `Avg Leads Per Day`.
        *   **Why:** To incorporate valuable business intelligence into the score, ensuring that proven, high-performing partners are ranked higher.
        *   **How:** By applying a multiplication factor to the base score based on the values in these columns.
    *   **Sub-Task 4.2.5:** Handle zero-overlap cases (Difficulty: 2/10)
        *   **What:** Ensure the function gracefully returns a score of 0 if there is no overlap at all between the partner and prospect codes.
        *   **Why:** To prevent errors and correctly handle non-matches.
        *   **How:** By having the function return `0` as a default or final `else` condition.

*   **Task 4.3: Run the Full Match** (Overall Difficulty: 4/10)
    *   **What:** Write the main part of the script that loads the two clean datasets and runs the scoring function on every possible pair.
    *   **Why:** To generate the raw data for the final report.
    *   **How:** The sub-tasks below detail the implementation.
    *   **Sub-Task 4.3.1:** Load the coded files (Difficulty: 2/10)
        *   **What:** Read `output/partners_with_codes.csv` and `output/prospects_with_codes.csv` into memory.
        *   **Why:** To get the necessary input data for the matching process.
        *   **How:** Using the `csv` library.
    *   **Sub-Task 4.3.2:** Implement the nested loop (Difficulty: 3/10)
        *   **What:** Write a `for` loop that iterates through each prospect, and inside it, another `for` loop that iterates through each partner.
        *   **Why:** To ensure that every prospect is compared against every partner.
        *   **How:** Using two nested `for` loops.
    *   **Sub-Task 4.3.3:** Call scoring and store results (Difficulty: 2/10)
        *   **What:** Inside the inner loop, call the `calculate_match_score()` function and store the resulting score, prospect, and partner information in a list.
        *   **Why:** To collect all the match scores for final processing.
        *   **How:** By calling the function and appending the result to a list of dictionaries, e.g., `results.append({'prospect': ..., 'partner': ..., 'score': ...})`.

*   **Task 4.4: Generate Final Report** (Difficulty: 3/10)
    *   **What:** After the main loop is complete, process the results list to find the top 5 partners for each prospect and write them to a final CSV file.
    *   **Why:** To produce the final, actionable output of the project.
    *   **How:** By first sorting the results list, then using a loop and a counter to select the top 5 matches for each prospect, and finally writing those rows to `output/matches_v1.csv`.

---
## **Phase 5: Maintenance & Tuning**
*Goal: Establish a long-term process for improving the system's accuracy and relevance.*

*   **Task 5.1: Establish Weekly Log Review** (Difficulty: 2/10)
    *   **What:** A recurring, human-driven process to analyze the `logs/unknown_log.csv` file.
    *   **Why:** To continuously improve the taxonomy by identifying new, emerging audience categories that the AI couldn't classify.
    *   **How:** By setting a weekly calendar reminder to open the log file. If a pattern is spotted (e.g., 3 or more similar companies are marked as `UNKNOWN`), a decision can be made to add a new code to the taxonomy.

*   **Task 5.2: Institute Score Tuning Loop** (Overall Difficulty: 6/10)
    *   **What:** A recurring, human-driven process to analyze the quality of the final matches and adjust the scoring weights to improve them.
    *   **Why:** Because the initial weights are just an educated guess. Real-world results are needed to fine-tune the scoring logic to produce the most commercially relevant matches.
    *   **How:** The sub-tasks below detail the implementation.
    *   **Sub-Task 5.2.1:** Manually review the final CSV (Difficulty: 2/10)
        *   **What:** Open `output/matches_v1.csv` and use human judgment to assess whether the top-ranked partners for a given prospect "feel" right.
        *   **Why:** To gather qualitative data on the performance of the scoring algorithm.
        *   **How:** By reading the file and applying domain expertise.
    *   **Sub-Task 5.2.2:** Formulate a hypothesis (Difficulty: 3/10)
        *   **What:** Based on the review, form a specific, testable hypothesis for improvement. For example: "The `Evaluation Score` boost is too powerful and is overriding good vertical matches."
        *   **Why:** A clear hypothesis guides the tuning process and prevents random, unproductive changes.
        *   **How:** Through critical thinking and analysis of the results.
    *   **Sub-Task 5.2.3:** Adjust weighting constants (Difficulty: 1/10)
        *   **What:** Make a small, targeted change to the scoring weight constants defined in `scripts/run_matching.py` to test the hypothesis.
        *   **Why:** To implement the proposed change in the code.
        *   **How:** By editing the value of a single variable (e.g., `EVALUATION_BOOST = 0.15`).
    *   **Sub-Task 5.2.4:** Re-run and compare (Difficulty: 3/10)
        *   **What:** Re-run the matching script (`scripts/run_matching.py`) to generate a new `matches_v2.csv`. Compare the new results to the old ones.
        *   **Why:** To empirically validate whether the change improved the results. This is the core of the scientific, iterative tuning process.
        *   **How:** By running the script and using a file comparison tool (or manual inspection) to see if the new rankings are better.