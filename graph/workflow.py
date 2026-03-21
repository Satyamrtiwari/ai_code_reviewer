from langgraph.graph import StateGraph, END
from graph.state import CodeReviewState

from agents.ast_analyzer import ast_analyzer
from agents.bug_detector import bug_detector
from agents.quality_reviewer import quality_reviewer
from agents.report_generator import report_generator
from agents.code_rewriter import code_rewriter

def create_workflow():
    # baseic workflow setup
    workflow = StateGraph(CodeReviewState)

    # add the nodes (our agents)
    workflow.add_node("ast_analyzer", ast_analyzer)
    workflow.add_node("bug_detector", bug_detector)
    workflow.add_node("quality_reviewer", quality_reviewer)
    workflow.add_node("report_generator", report_generator)
    workflow.add_node("code_rewriter", code_rewriter)

    # connect the dots
    workflow.set_entry_point("ast_analyzer")
    workflow.add_edge("ast_analyzer", "bug_detector")
    workflow.add_edge("bug_detector", "quality_reviewer")
    workflow.add_edge("quality_reviewer", "report_generator")
    workflow.add_edge("report_generator", "code_rewriter")
    workflow.add_edge("code_rewriter", END)

    return workflow.compile()
