import sys
import os
import json

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classifier import classify_blurb

def test_single_blurb_classification():
    """
    Tests the classification of a single, hardcoded blurb to inspect
    the full input and output of the LLM call.
    """
    test_description = "HRlab is a company in the Human Resources sector. They offer HR Software. Their unique selling proposition is: HRlab is a clear and simple HR software that simplifies all operational HR processes and digitizes the entire employee lifecycle."

    print(f"--- Testing with description ---\n{test_description}\n")

    # Call the classification function
    result = classify_blurb(test_description)

    # Print the final, parsed result
    print("\n----------- FINAL PARSED RESULT -----------")
    print(json.dumps(result, indent=2))
    print("------------------------------------")

    # Add a simple assertion to ensure the test provides a clear pass/fail
    assert "error" not in result, f"Test failed with error: {result.get('error')}"
    assert "primary" in result, "Test failed: 'primary' key missing from result."
    assert "secondary" in result, "Test "

if __name__ == "__main__":
    test_single_blurb_classification()