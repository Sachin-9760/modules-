from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import CandidateState
from .nodes import (
    evaluate_candidate,
    route_candidate,
    human_review,
    route_human_decision,
    approve_candidate,
    reject_candidate,
)

def build_graph():
    builder = StateGraph(CandidateState)

    builder.add_node("evaluate", evaluate_candidate)
    builder.add_node("human_review", human_review)
    builder.add_node("approve", approve_candidate)
    builder.add_node("reject", reject_candidate)

    builder.add_edge(START, "evaluate")

    builder.add_conditional_edges(
        "evaluate",
        route_candidate,
        {
            "human_review": "human_review",
            "reject": "reject",
        },
    )

    builder.add_conditional_edges(
        "human_review",
        route_human_decision,
        {
            "approve": "approve",
            "reject": "reject",
        },
    )

    builder.add_edge("approve", END)
    builder.add_edge("reject", END)

    # Checkpointing is required for interrupt/resume.
    return builder.compile(checkpointer=MemorySaver())
