from typing import TypedDict

class CandidateState(TypedDict, total=False):
    candidate_id: int
    candidate_name: str
    skills: list[str]
    experience: float
    score: int
    human_review: str
    decision: str
    status: str
