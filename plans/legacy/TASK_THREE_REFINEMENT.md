# Refinement for Phase 3: Prospect Enrichment & Classification

This document details the updated, more robust plan for Phase 3. It replaces the previous method of using a single CSV column with a superior two-step LLM process that leverages scraped webpage content for higher accuracy.

---
### **Phase 3: Prospect Enrichment & Classification (v2)**
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