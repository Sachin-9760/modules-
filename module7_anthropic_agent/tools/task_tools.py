TASKS = {
    1: {"id": 1, "title": "Build FastAPI API", "status": "completed", "priority": "high"},
    2: {"id": 2, "title": "Connect PostgreSQL", "status": "in progress", "priority": "high"},
    3: {"id": 3, "title": "Configure Redis", "status": "pending", "priority": "medium"},
    4: {"id": 4, "title": "Build AI Agent", "status": "in progress", "priority": "high"},
}

def get_task(task_id: int) -> dict:
    task = TASKS.get(task_id)
    if not task:
        return {"found": False, "message": f"Task {task_id} was not found."}
    return {"found": True, "task": task}

def list_tasks() -> dict:
    return {"count": len(TASKS), "tasks": list(TASKS.values())}
