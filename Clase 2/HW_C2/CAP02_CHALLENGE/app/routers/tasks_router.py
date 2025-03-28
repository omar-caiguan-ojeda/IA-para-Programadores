"""
FastAPI router for task management operations.

This router provides endpoints for creating, retrieving, updating, and deleting tasks.

Endpoints:
- POST /: Create a new task
- GET /{task_id}: Retrieve a specific task by ID
- GET /: Retrieve all tasks
- PUT /{task_id}: Update an existing task
- DELETE /{task_id}: Delete a specific task
- DELETE /: Delete all tasks
"""
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


@tasks_router.delete("/{task_id}", status_code=200)
async def delete_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}


@tasks_router.delete("/", status_code=204)
async def delete_all_tasks():
    """Elimina todas las tareas de la base de datos."""
    db.tasks.clear()
    return None


# SUGERIDO POR CODY :

# @router.delete("/{task_id}", status_code=status.HTTP_200_OK)
# def delete_task(task_id: int, db: Session = Depends(get_db)):
#     task = db.query(Task).filter(Task.id == task_id).first()
#     if task is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Tarea no encontrada"
#         )
    
#     db.delete(task)
#     db.commit()
#     return {"message": "Tarea eliminada correctamente"}

# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# def delete_all_tasks(db: Session = Depends(get_db)):
#     """Elimina todas las tareas de la base de datos."""
#     db.query(Task).delete()
#     db.commit()
#     return None