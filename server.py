from fastapi import FastAPI
from pydantic import BaseModel

from agents.agent import agent

app = FastAPI()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": request.question}
        ]
    })

    return {"answer": result["messages"][-1].content}