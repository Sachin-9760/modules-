from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
import asyncio
import json


DATABASE_URL = "postgresql://postgres:sachin@obbservlocalhost:5432/module4_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Module 4 Mini Project")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Module 4 API is running"}


@app.post("/tasks")
def create_task(title: str, db: Session = Depends(get_db)):
    task = Task(title=title, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)

    data = {"id": task.id, "title": task.title, "status": task.status}
    redis_client.setex(f"task:{task.id}", 60, json.dumps(data))

    return data


@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    cached = redis_client.get(f"task:{task_id}")

    if cached:
        return {"source": "redis", "task": json.loads(cached)}

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    data = {"id": task.id, "title": task.title, "status": task.status}
    redis_client.setex(f"task:{task.id}", 60, json.dumps(data))

    return {"source": "postgresql", "task": data}


@app.websocket("/ws/tasks/{task_id}")
async def task_progress(websocket: WebSocket, task_id: int):
    await websocket.accept()

    for progress in range(0, 101, 20):
        await websocket.send_json({
            "task_id": task_id,
            "progress": progress,
            "status": "completed" if progress == 100 else "processing"
        })
        await asyncio.sleep(1)

    await websocket.close()
