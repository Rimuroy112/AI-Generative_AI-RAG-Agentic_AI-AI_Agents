from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange
from typing import Optional

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None

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
        
@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"Post with id: {id} was not found"}
    print(post)
    return {"post_details": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_post(id)
    my_posts.pop(index)
    return{'message':'Post was successfully deleted'}