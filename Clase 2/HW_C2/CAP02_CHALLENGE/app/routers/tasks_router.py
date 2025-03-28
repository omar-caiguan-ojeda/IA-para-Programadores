from fastapi import APIRouter, HTTPException
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()


@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)


@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)


@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}
