import json
from langchain_core.prompts import ChatPromptTemplate
from graph.state import CodeReviewState
from utils.groq_client import get_groq_llm

# this agent rewrites the code properly using groq
def code_rewriter(state: CodeReviewState):
    code = state.get("code", "")
    language = state.get("language", "Python")
    bugs = state.get("bugs", [])
    quality = state.get("quality_review", {})

    if not code.strip():
        state["rewritten_code"] = ""
        return state

    suggestions = quality.get("suggestions", [])
    bug_list = [b.get("issue", "") for b in bugs]

    prompt_template = """
    You are an expert {language} developer.
    Rewrite the following {language} code to fix all bugs, apply all suggestions, and follow best practices.

    Original Code:
    ```{language}
    {code}
    ```

    Known Bugs to Fix:
    {bugs}

    Suggestions to Apply:
    {suggestions}

    Rules:
    - Output ONLY the rewritten code, no explanation, no markdown fences.
    - Keep the same logic and structure, just fix and improve it.
    - Add docstrings/comments where missing.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    try:
        llm = get_groq_llm()
        chain = prompt | llm
        response = chain.invoke({
            "code": code,
            "language": language,
            "bugs": json.dumps(bug_list),
            "suggestions": json.dumps(suggestions[:5])
        })
        state["rewritten_code"] = response.content.strip()
    except Exception as e:
        state["rewritten_code"] = f"# Error during rewrite: {str(e)}"

    return state
