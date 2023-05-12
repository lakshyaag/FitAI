import os
import json

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from parser_class import WorkoutPlan

load_dotenv(find_dotenv())

openai_api_key = os.environ.get("OPENAI_API_KEY")

system_message = SystemMessagePromptTemplate.from_template(
    """Your task is to act as a personal fitness trainer. You will be provided with information about your CLIENT's current fitness level, their goals, and other preferences they have. You have to prepare a detailed workout plan for the CLIENT, including everything essential for fitness."""  # noqa: E501
)


@st.cache_data()
def load_questions():
    with open("./questions.json") as f:
        questions_list = json.load(f)["questions"]
    return questions_list


def generate_question_answer(question):
    question_text = question["text"]
    answer_choices = question["options"]

    return st.selectbox(label=f"**{question_text}**", options=answer_choices)


@st.cache_data()
def question_message(questions_list):
    question_message = HumanMessagePromptTemplate.from_template(
        f'The list of questions that have been asked to the CLIENT (separated by a ;) are: \n{";".join(i["text"] for i in questions_list)}'  # noqa: E501
    )

    return question_message


@st.cache_data()
def answer_message(answers):
    answer_message = HumanMessagePromptTemplate.from_template(
        f'The answers provided by the CLIENT (separated by a ;) are: \n{";".join(answers)}'  # noqa: E501
    )

    return answer_message


@st.cache_data()
def format_message():
    format_message = HumanMessagePromptTemplate.from_template(
        template="""With the given details, proceed to create a detailed weekly plan that can be followed for 2 months for the CLIENT, making sure to incorporate their inputs properly.
    Ensure that you include cardio and rest time inside the plan as part of the `exercise` object. Try to keep the notes section as generic as possible as most CLIENTS will not read it.
    {format_instructions}""",  # noqa: E501
    )

    return format_message


@st.cache_data()
def generate_parser():
    parser = PydanticOutputParser(pydantic_object=WorkoutPlan)

    return parser


@st.cache_data()
def generate_prompt(questions_list, answers, format_instructions):
    print(question_message(questions_list))

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message,
            question_message(questions_list),
            answer_message(answers),
            format_message(),
        ]
    )

    messages = chat_prompt.format_prompt(
        format_instructions=format_instructions,
    ).to_messages()

    return messages


def call_gpt(prompt):
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.4,
        openai_api_key=openai_api_key,
        verbose=True,
    )

    response = chat(prompt)

    return response


def parse_response(response, parser):
    plan = parser.parse(response.content)
    return plan


def print_plan(plan):
    for p in plan.weeks:
        st.write(f"Week: {p.week_range}")
        for day in p.days:
            st.write(f"Day: {day.day_number}\nFocus: {day.focus}")
            st.write(
                [
                    f"{exercise.name} -> {exercise.sets} x {exercise.reps} x {exercise.duration}"  # noqa: E501
                    for exercise in day.exercises
                ]
            )

    st.write(plan.notes)
