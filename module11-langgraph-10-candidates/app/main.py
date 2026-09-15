from langgraph.types import Command

if __package__ in {None, ""}:
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from app.graph import build_graph
    from app.database import init_db, save_result
else:
    from .graph import build_graph
    from .database import init_db, save_result

CANDIDATES = [
    {"candidate_id": 1, "candidate_name": "Rahul", "skills": ["Python", "SQL", "LangChain", "LangGraph"], "experience": 2.0},
    {"candidate_id": 2, "candidate_name": "Amit", "skills": ["Java", "SQL", "Spring"], "experience": 2.0},
    {"candidate_id": 3, "candidate_name": "Priya", "skills": ["Python", "React", "SQL", "LangGraph"], "experience": 3.0},
    {"candidate_id": 4, "candidate_name": "Neha", "skills": ["HTML", "CSS", "JavaScript"], "experience": 1.0},
    {"candidate_id": 5, "candidate_name": "Vikas", "skills": ["Python", "Django", "SQL"], "experience": 4.0},
    {"candidate_id": 6, "candidate_name": "Anjali", "skills": ["Java", "Spring", "SQL", "React"], "experience": 3.0},
    {"candidate_id": 7, "candidate_name": "Rohit", "skills": ["C++", "Python"], "experience": 1.0},
    {"candidate_id": 8, "candidate_name": "Pooja", "skills": ["Python", "SQL", "LangChain", "React"], "experience": 2.0},
    {"candidate_id": 9, "candidate_name": "Karan", "skills": ["JavaScript", "Node.js", "SQL", "React"], "experience": 3.0},
    {"candidate_id": 10, "candidate_name": "Simran", "skills": ["Python", "SQL", "LangGraph", "FastAPI"], "experience": 4.0},
]

def process_candidate(candidate):
    graph = build_graph()
    thread_id = f"candidate-{candidate['candidate_id']}"
    config = {"configurable": {"thread_id": thread_id}}

    state = {
        **candidate,
        "decision": "",
        "human_review": "",
        "status": "new",
    }

    result = graph.invoke(state, config=config)

    if "__interrupt__" in result:
        info = result["__interrupt__"][0].value
        print("\n--- HUMAN REVIEW CHECKPOINT ---")
        print("Candidate:", info["candidate"])
        print("Score:", info["score"])
        answer = input("Approve candidate? (yes/no): ").strip().lower()

        result = graph.invoke(Command(resume=answer), config=config)

    print(f"Result: {result.get('candidate_name')} -> {result.get('decision')}")
    save_result(result)

def main():
    init_db()

    print("\n=== Module 11: 10 Candidate LangGraph Screening ===")
    print("10 candidates will be processed.")
    print("For candidates with score >= 70, you will manually choose YES or NO.")

    for candidate in CANDIDATES:
        print("\n========================================")
        print(f"Candidate {candidate['candidate_id']}: {candidate['candidate_name']}")
        print("Skills:", ", ".join(candidate["skills"]))
        print("Experience:", candidate["experience"], "years")
        process_candidate(candidate)

    print("\nAll 10 candidates processed.")
    print("Run 'python -m app.history' to see who was approved/rejected.")

if __name__ == "__main__":
    main()
