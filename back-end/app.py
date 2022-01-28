from os import link
from sqlite3 import Binary
from typing import Optional
from nturl2path import url2pathname
from typing import Optional, Set
from fastapi import FastAPI, HTTPException, status, responses
from fastapi.middleware.cors import CORSMiddleware
from pydantic.dataclasses import dataclass
from setuptools import Require
from pony.orm import Database, PrimaryKey, Required, db_session, set_sql_debug
from typing import Optional


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database(provider='sqlite', filename='database.db', create_db=True)


class User(db.Entity):
    _table_ = "Users"
    id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    salary = Required(int)
    image = Required(str)


db.generate_mapping(create_tables=True)
set_sql_debug(True)


@dataclass
class UserDTO():
    first_name: str
    salary: int
    image: str


@app.get("/api/users")
def getUsers():
    users = None
    with db_session:
        users = User.select()
        return [u.to_dict() for u in users]


@app.get("/api/users/{id}")
def getUser(id: int):
    with db_session:
        if User.exists(id=id):
            return User[id]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int):
    with db_session():
        if User.exists(id=id):
            User[id].delete()
        else:
            raise HTTPException(
                status_code=404, detail=f"User with id of {id} not found")
        db.commit()
        return {"msg": "deleted"}


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def createUser(user: UserDTO):
    with db_session:
        User(first_name=user.first_name,
             salary=user.salary, image=user.image)
        db.commit()
        return {"message": "user was created"}


@app.put("/api/users/{id}")
def updateUser(id: int, user: UserDTO):
    with db_session:
        user = User[id]
        user.first_name = user.first_name
        user.salary = user.salary
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id of {id} not found")
        print(user.to_dict())
        db.commit()

        return {"updated": "updated"}
