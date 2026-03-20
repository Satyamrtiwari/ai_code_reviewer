import json
from langchain_core.prompts import ChatPromptTemplate
from graph.state import CodeReviewState
from utils.groq_client import get_groq_llm

# this agent uses groq to find bugs in the code
def bug_detector(state: CodeReviewState):
    code = state.get("code", "")
    ast_analysis = state.get("ast_analysis", {})
    language = state.get("language", "Python")

    if not code.strip():
        state["bugs"] = []
        return state

    # prompt for the llm
    prompt_template = """
    You are an expert {language} security and bug detection AI. 
    Analyze the following {language} code and identify any:
    1. Logical errors
    2. Potential runtime errors / unhandled exceptions
    3. Unused variables
    4. Security issues (e.g., hardcoded secrets, SQL injection vulnerabilities)

    Code:
    ```python
    {code}
    ```
    
    AST Analysis Information:
    {ast_analysis}
    
    Output a JSON list of dictionaries. Each dictionary must have the following keys:
    - line_number: The line number where the issue occurs (if applicable, else 0 or approximation)
    - issue: A short description of the bug or vulnerability
    - severity: HIGH, MEDIUM, or LOW
    
    Do NOT output anything else except the JSON array.
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    try:
        llm = get_groq_llm()
        chain = prompt | llm
        
        response = chain.invoke({
            "code": code,
            "ast_analysis": json.dumps(ast_analysis),
            "language": language
        })
        
        # Parse the JSON response
        # Sometimes the LLM wraps JSON in markdown code blocks
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        bugs = json.loads(content.strip())
        state["bugs"] = bugs if isinstance(bugs, list) else []
        
    except Exception as e:
        state["bugs"] = [{
            "line_number": 0,
            "issue": f"Error during bug detection LLM call: {str(e)}",
            "severity": "HIGH"
        }]

    return state
