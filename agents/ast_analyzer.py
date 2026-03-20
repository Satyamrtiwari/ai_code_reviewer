import ast
from graph.state import CodeReviewState

# this agent do the baseic static analysis
# we extract things like class names and stuff
def ast_analyzer(state: CodeReviewState):
    code = state.get("code", "")
    language = state.get("language", "Python")
    
    analysis = {
        "function_names": [],
        "class_names": [],
        "num_lines": len(code.splitlines()) if code else 0,
        "imports": [],
        "issues": []
    }

    if not code.strip() or language != "Python":
        if language != "Python":
            analysis["issues"].append(f"AST skiped for {language} (only works for python).")
        state["ast_analysis"] = analysis
        return state

    try:
        tree = ast.parse(code)
        
        # walk the tree
        for node in ast.walk(tree):
            # Extract Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    analysis["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    analysis["imports"].append(node.module)
            
            # Extract Classes
            elif isinstance(node, ast.ClassDef):
                analysis["class_names"].append(node.name)
                # Check for docstrings
                if not ast.get_docstring(node):
                    analysis["issues"].append(f"Class '{node.name}' is missing a docstring.")
            
            # Extract Functions
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                analysis["function_names"].append(node.name)
                
                # Check for docstrings
                if not ast.get_docstring(node):
                    analysis["issues"].append(f"Function '{node.name}' is missing a docstring.")
                
                # Check for number of parameters
                num_params = len(node.args.args)
                if num_params > 5:
                    analysis["issues"].append(f"Function '{node.name}' has too many parameters ({num_params} > 5).")
                
                # Check for function length (approximate using line numbers if available)
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    func_length = node.end_lineno - node.lineno
                    if func_length > 50:
                        analysis["issues"].append(f"Function '{node.name}' is too long ({func_length} lines > 50).")

    except SyntaxError as e:
        analysis["issues"].append(f"Syntax Error: Could not parse code. Details: {str(e)}")
    except Exception as e:
        analysis["issues"].append(f"AST Analysis Error: {str(e)}")

    # Update state
    state["ast_analysis"] = analysis
    return state
