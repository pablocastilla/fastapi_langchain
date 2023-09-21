# this module is the backend of the app
# it exposes a fastapi post endpoint

from typing import Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from app.llms.Illm import ILLM
from app.llms.open_ai_llm_logic import OpenAILLMLogic
import uuid

from app.queue_management.memory_queue_management_system import MemoryQueueManagementSystem


class Input(BaseModel):
    human_input: str


class Output(BaseModel):
    output: str


app = FastAPI()


@app.middleware("http")
async def some_middleware(request: Request, call_next: Any) -> Any:
    response = await call_next(request)
    session = request.cookies.get('session')
    if not session:
        # set the cookie with a guid as value
        response.set_cookie(key='session', value=uuid.uuid4(), httponly=True)
    return response


@app.post("/conversation")
async def input(input: Input) -> Output:
    llm_logic: ILLM = OpenAILLMLogic(queue_management_system=MemoryQueueManagementSystem())
    with llm_logic:
        response = await llm_logic.chat(input.human_input)
        return Output(output=response)


origins = [
    "<http://localhost>",
    "<http://localhost:5173>"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
