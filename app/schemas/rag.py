from pydantic import BaseModel

class AskIn(BaseModel):
    question: str

class AskOut(BaseModel):
    answer: str