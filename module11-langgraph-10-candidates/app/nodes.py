from langgraph.types import interrupt
from .state import CandidateState

def evaluate_candidate(state: CandidateState) -> CandidateState:
    skills = state.get("skills", [])
    experience = state.get("experience", 0)

    # Simple scoring for learning LangGraph.
    score = min(100, len(skills) * 15 + int(experience * 10))

    return {
        **state,
        "score": score,
        "status": "evaluated",
    }

def route_candidate(state: CandidateState) -> str:
    return "human_review" if state.get("score", 0) >= 70 else "reject"

def human_review(state: CandidateState) -> CandidateState:
    # LangGraph pauses here and saves the graph state.
    answer = interrupt({
        "message": "Human review required",
        "candidate": state.get("candidate_name"),
        "score": state.get("score"),
        "question": "Approve this candidate? Type yes or no.",
    })

    return {
        **state,
        "human_review": str(answer),
        "status": "human_review_completed",
    }

def route_human_decision(state: CandidateState) -> str:
    answer = state.get("human_review", "").strip().lower()
    return "approve" if answer in {"yes", "y", "approve", "approved"} else "reject"

def approve_candidate(state: CandidateState) -> CandidateState:
    return {**state, "decision": "approved", "status": "completed"}

def reject_candidate(state: CandidateState) -> CandidateState:
    return {**state, "decision": "rejected", "status": "completed"}
