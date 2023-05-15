import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Union, List

import api_utils as utils


class Request(BaseModel):
    answer: Dict[str, Union[str, List[str]]]


app = FastAPI()

questions_list = utils.load_questions()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate/")
def get_workout_plan(answers: Request):
    qa_messages = utils.generate_qa_messages(
        questions_list=questions_list, answers=answers.answer
    )

    prompts = utils.generate_prompt(qa_messages=qa_messages)

    response = utils.call_gpt(prompt=prompts, model="gpt-4")

    parsed_response = utils.parse_response(response=response)

    return parsed_response


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
