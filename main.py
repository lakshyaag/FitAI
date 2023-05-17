import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Union, List

import api_utils as utils


class Request(BaseModel):
    answer: Dict[str, Union[str, List[str]]]


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"])

questions_list = utils.load_questions()


@app.get("/")
def root():
    return {
        "message": "Welcome to the FitAI backend. Please refer to /docs for more info."
    }


@app.post("/generate/")
def get_workout_plan(answers: Request):
    qa_messages = utils.generate_qa_messages(
        questions_list=questions_list, answers=answers.answer
    )

    prompts = utils.generate_prompt(qa_messages=qa_messages)

    response = utils.call_gpt(prompt=prompts, model="gpt-3.5-turbo")

    parsed_response = utils.parse_response(response=response)

    return parsed_response


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
