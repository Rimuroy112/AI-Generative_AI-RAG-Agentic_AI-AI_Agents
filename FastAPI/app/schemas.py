from pydantic import BaseModel

class post(BaseModel):
    title: str
    content: str
    published: bool=True
