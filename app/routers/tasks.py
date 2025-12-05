from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Task
from ..schemas import TaskCreate, TaskOut
from ..auth import get_current_user

router = APIRouter()

@router.post("/tasks")
def add_task(task: TaskCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description, user_id=user.id)
    db.add(new_task)
    db.commit()
    return {"message": "Task added successfully"}

@router.get("/tasks")
def get_tasks(user=Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}/complete")
def complete(task_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    db.commit()
    return {"message": "Task completed successfully"}

@router.delete("/tasks/{task_id}")
def delete(task_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
