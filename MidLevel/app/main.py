from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="MidLevel API")

# 示例数据模型
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# 内存中的任务列表（实际应用中会使用数据库）
tasks: List[Task] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to MidLevel API"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id < len(tasks):
        return tasks[task_id]
    return {"error": "Task not found"}