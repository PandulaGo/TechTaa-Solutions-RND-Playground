from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel): # - Define a Pydantic model for creating a new task. This model will be used to validate the input data when creating a new task.
    title:str = Field(min_length=1, max_length=255)

class  TaskUpdate(BaseModel): # - Define a Pydantic model for updating an existing task. This model will be used to validate the input data when updating a task. The fields are optional, allowing partial updates.
    title:str | None = Field(default=None, min_length=1, max_length=255)
    done:bool | None = None

class TaskOut(BaseModel): # - Define a Pydantic model for representing a task when sending it as a response. This model includes all the fields of a task, including the ID and creation timestamp. The `from_attributes` configuration allows the model to be created from ORM objects directly.
    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str
    done:bool
    created_at:datetime