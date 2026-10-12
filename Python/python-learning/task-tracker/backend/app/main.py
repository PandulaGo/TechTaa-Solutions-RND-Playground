from fastapi import Depends, FastAPI, HTTPException # - Import the FastAPI class and the Depends function from the fastapi module. The FastAPI class is used to create the application instance, while Depends is used for dependency injection, allowing you to define dependencies for your route handlers.
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import models,schemas
from .database import get_db

from fastapi.middleware.cors import CORSMiddleware

# Removing the engine creation and Base.metadata.create_all(bind=engine) from this file, as it is not necessary to create the database tables here. The database tables should be created using Alembic migrations, which are handled in the migrations/env.py file. This ensures that the database schema is managed consistently and allows for version control of the database structure.

#Base.metadata.create_all(bind=engine) # - Create all the database tables defined in the ORM models. This line ensures that the database schema is created based on the models defined in the `models` module. It uses the metadata of the Base class to create the tables in the database specified by the engine.

app = FastAPI(
    title="Task Tracker API", 
    description="API for managing tasks", 
    version="1.0.0"
) # - Create an instance of the FastAPI application with a title, description, and version. This instance will be used to define routes and handle incoming HTTP requests.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)): # - Define an endpoint to check the database connection. It uses dependency injection to get a database session from the `get_db` function. The session is used to execute a simple SQL query to verify that the database connection is working. If the query executes successfully, it returns a success message; otherwise, it returns an error message with details about the failure.
    try:
        db.execute(text("SELECT 1"))
        return {"status": "database connection successful"}
    except Exception as e:
        return {"status": "database connection failed", "error": str(e)}  

@app.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(models.Task).order_by(models.Task.id)).all() # - Define a GET endpoint at the path "/tasks" to retrieve a list of tasks from the database. It uses dependency injection to get a database session from the `get_db` function. The endpoint executes a SQL query to select all tasks from the "tasks" table, ordered by their ID, and returns the result as a list of `TaskOut` Pydantic models.

@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(title=payload.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task # - Define a POST endpoint at the path "/tasks" to create a new task in the database. It uses dependency injection to get a database session from the `get_db` function. The endpoint receives a payload of type `TaskCreate`, creates a new `Task` instance with the provided title, adds it to the database session, commits the transaction, refreshes the task instance to get its updated state (including the generated ID), and returns the created task as a `TaskOut` Pydantic model. The response status code is set to 201 (Created).

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None
