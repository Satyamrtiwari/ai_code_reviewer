from graph.state import CodeReviewState

# this agent gathers everything and makes the final report
def report_generator(state: CodeReviewState):
    ast_analysis = state.get("ast_analysis", {})
    bugs = state.get("bugs", [])
    quality = state.get("quality_review", {})
    language = state.get("language", "Python")
    
    score = quality.get("score", 0)
    suggestions = quality.get("suggestions", [])
    complexity = quality.get("complexity", [])
    issues = ast_analysis.get("issues", [])
    
    # build the summary
    summary = f"This {language} code contains {ast_analysis.get('num_lines', 0)} lines. "
    if language == "Python":
        summary += (
            f"It has {len(ast_analysis.get('class_names', []))} classes and "
            f"{len(ast_analysis.get('function_names', []))} functions. "
        )
        
    if score >= 90:
        summary += "Overall, the code quality is excellent, with minimal issues."
    elif score >= 70:
        summary += "The code is structurally sound but has several areas for improvement."
    else:
        summary += "The code requires significant refactoring to meet production standards."

    # Building the Markdown Report
    report = []
    
    # 1. Overview & Score
    report.append("## Overview & Score\n")
    report.append(summary + "\n")
    report.append(f"**Overall Quality Score:** {score}/100\n")
    
    if issues:
        report.append("### Structural Warnings\n")
        for issue in issues:
            report.append(f"- ⚠️ {issue}")
        report.append("\n")

    # 2. Bug Report
    report.append("## Bug Report\n")
    if not bugs:
        report.append("✅ No bugs detected!\n")
    else:
        for bug in bugs:
            severity = bug.get('severity', 'LOW').upper()
            icon = "🔴" if severity == "HIGH" else "🟠" if severity == "MEDIUM" else "🟡"
            line = bug.get('line_number', 'N/A')
            issue_desc = bug.get('issue', 'Unknown issue')
            report.append(f"- {icon} **{severity}** (Line {line}): {issue_desc}")
    report.append("\n")

    # 3. Improvement Suggestions
    report.append("## Improvement Suggestions\n")
    if not suggestions:
        report.append("✅ No further suggestions.\n")
    else:
        for i, suggestion in enumerate(suggestions[:5], 1): # Top 5 suggestions
            report.append(f"{i}. {suggestion}")
    report.append("\n")

    # 4. Complexity Analysis
    report.append("## Complexity Analysis\n")
    if not complexity:
        report.append("No complexity metrics available.\n")
    else:
        report.append("| Element Name | Type | Cyclomatic Complexity |")
        report.append("| --- | --- | --- |")
        for item in complexity:
            name = item.get("name", "Unknown")
            ctype = item.get("type", "Unknown")
            cc = item.get("complexity", 1)
            report.append(f"| {name} | {ctype} | {cc} |")

    state["final_report"] = "\n".join(report)
    return state
