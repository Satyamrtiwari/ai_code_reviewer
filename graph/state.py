from typing import TypedDict, List, Dict

class CodeReviewState(TypedDict):
    # defineing the state for our agents
    code: str                  # the code we gota review
    language: str              # the language
    ast_analysis: dict         # ast results
    bugs: list                 # bug list
    quality_review: dict       # quality score n stuff
    final_report: str          # markdown reportore and suggestions from Quality Reviewer
