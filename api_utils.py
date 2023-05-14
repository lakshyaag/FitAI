import json
import os

import yaml
from dotenv import find_dotenv, load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from prompts import (
    EXAMPLE_RESPONSE,
    SCHEMA,
    first_message,
    format_message,
    qa_message,
    schema_message,
    system_message,
)
from workout import WorkoutPlan

load_dotenv(find_dotenv())

openai_api_key = os.environ.get("OPENAI_API_KEY")


def load_questions():
    with open("./questions.json") as f:
        questions_list = json.load(f)["questions"]
    return questions_list


def generate_qa_messages(questions_list, answers):
    qa_messages = [
        qa_message.format(question=q["text"], answer=answers[i])
        for i, q in enumerate(questions_list)
    ]
    return qa_messages


def generate_prompt(qa_messages):
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message,
            first_message,
            format_message,
            schema_message,
        ]
    )

    messages = chat_prompt.format_prompt(
        example_response=EXAMPLE_RESPONSE,
        output_schema=SCHEMA,
    ).to_messages()

    for x in reversed(qa_messages):
        messages.insert(1, x)

    return messages


def call_gpt(prompt, model="gpt-4"):
    chat = ChatOpenAI(
        model_name=model,
        temperature=0.2,
        openai_api_key=openai_api_key,
        verbose=True,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )

    # st.write(prompt)
    response = chat(prompt)

    return response


def parse_response(response):
    response_json = yaml.safe_load(response.content)

    plan = WorkoutPlan(**response_json["WorkoutPlan"])
    return plan
