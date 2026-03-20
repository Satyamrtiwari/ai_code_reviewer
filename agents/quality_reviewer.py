import json
from radon.complexity import cc_visit
from langchain_core.prompts import ChatPromptTemplate
from graph.state import CodeReviewState
from utils.groq_client import get_groq_llm

def quality_reviewer(state: CodeReviewState):
    """
    Agent 3: Code Quality Reviewer
    Uses Groq LLM to check readability, PEP8, and SOLID principles.
    Uses radon to calculate cyclomatic complexity.
    """
    code = state.get("code", "")
    language = state.get("language", "Python")
    
    if not code.strip():
        state["quality_review"] = {"score": 0, "suggestions": [], "complexity": []}
        return state

    # Step 1: Radon complexity (Only if python)
    complexity_results = []
    if language == "Python":
        try:
            blocks = cc_visit(code)
            for block in blocks:
                complexity_results.append({
                    "name": block.name,
                    "complexity": block.complexity,
                    "type": type(block).__name__
                })
        except Exception as e:
            complexity_results.append({"name": "Error", "complexity": str(e), "type": "Error"})
    else:
        complexity_results.append({"name": f"N/A ({language})", "complexity": "N/A", "type": "Skipped"})

    # Step 2: Quality Review with LLM
    prompt_template = """
    You are an expert {language} developer and code quality reviewer.
    Review the following {language} code for:
    1. Readability and naming conventions
    2. Code duplication (DRY principle)
    3. PEP8 violations
    4. Compliance with SOLID principles
    
    Code:
    ```python
    {code}
    ```
    
    Provide an overall quality score out of 100 and a list of specific improvement suggestions.
    Output a JSON object with EXACTLY these keys:
    - score: An integer from 0 to 100.
    - suggestions: A list of strings, each containing a specific suggestion (include code rewrite snippets if applicable).
    
    Do NOT output anything else except the JSON object.
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    try:
        llm = get_groq_llm()
        chain = prompt | llm
        
        response = chain.invoke({
            "code": code,
            "language": language
        })
        
        # Parse the JSON response
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        review = json.loads(content.strip())
        suggestions = review.get("suggestions", [])
        score = review.get("score", 0)
        
    except Exception as e:
        score = 0
        suggestions = [f"Error during quality review LLM call: {str(e)}"]

    state["quality_review"] = {
        "score": score,
        "suggestions": suggestions,
        "complexity": complexity_results
    }
    
    return state
