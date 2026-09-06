from fastapi import FastAPI
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

@app.get("/posts")
def root():
    return {"data":my_posts}

@app.post("/posts")
def root(post: post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

