from fastapi import FastAPI,Response,status,HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class post(BaseModel):
    title: str
    content: str
    published: bool=True

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
        password='Postgres123;;;',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull !")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(2)
    
    

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"title of post 2","content":"content of post 2","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}
        
@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES( %s, %s, %s) RETURNING 
    * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"Post with id: {id} was not found"}
    print(post)
    return {"post_details": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id:int, post:post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not found")

    return {"data": updated_post}