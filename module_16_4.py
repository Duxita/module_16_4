from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
class User(BaseModel):
    id: int
    username: str
    age: int
app = FastAPI()
users: List[User] = []
@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int = Path(..., ge=1, le=100, description="Enter User ID")):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
@app.get("/user/{username}/{age}", response_model=str)
def get_user_info(
    username: Annotated[str, Path(min_length=5, max_length=20, pattern="^[A-Za-z0-9_-]+$", description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")],
):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"
@app.get("/users", response_model=List[User])
def get_users():
    return users
@app.post("/user/{username}/{age}", response_model=User)
def create_user(username: str, age: int):
    new_user_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")
@app.delete("/user/{user_id}", response_model=dict)
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            delete_user = users.pop(i)
            return {"detail": f"User ID :{delete_user} deleted!"}
    raise HTTPException(status_code=404, detail="User not found")