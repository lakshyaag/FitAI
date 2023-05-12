import os
import json

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from workout import WorkoutPlan

load_dotenv(find_dotenv())

openai_api_key = os.environ.get("OPENAI_API_KEY")

system_message = SystemMessagePromptTemplate.from_template(
    """Your task is to act as a personal fitness trainer. 
    You will be provided with information about your CLIENT's current fitness level, their goals, and other preferences they have. 
    You have to prepare a detailed workout plan for the CLIENT, including everything essential for physical fitness.
    Ensure that you strictly adhere to the number of days and weeks the CLIENT is willing to do their workout. Skip rest days from your output."""  # noqa: E501
)


@st.cache_data()
def load_questions():
    with open("./questions.json") as f:
        questions_list = json.load(f)["questions"]
    return questions_list


@st.cache_data()
def get_sections(questions_list):
    sections = [q["section"] for q in questions_list]

    return [*dict.fromkeys(sections)]


def generate_question_box(question):
    question_text = question["text"]

    if question["question_type"] == "single_select":
        answer_choices = question["options"]
        return st.selectbox(
            label=f"**{question_text}**", options=answer_choices, key=question["id"]
        )
    elif question["question_type"] == "open_text":
        return st.number_input(
            label=f"**{question_text}**",
            min_value=0.00,
            value=50.00,
            key=question["id"],
        )


@st.cache_data()
def question_message(questions_list):
    question_message = HumanMessagePromptTemplate.from_template(
        f'The list of questions that have been asked to the CLIENT (separated by a ;) are: \n{";".join(i["text"] for i in questions_list)}'  # noqa: E501
    )

    return question_message


@st.cache_data()
def answer_message(answers):
    answer_message = HumanMessagePromptTemplate.from_template(
        f'The answers provided by the CLIENT (separated by a ;) are: \n{";".join(map(str, answers))}'  # noqa: E501
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


def call_gpt(prompt, model="gpt-3.5-turbo"):
    chat = ChatOpenAI(
        model_name=model,
        temperature=0.4,
        openai_api_key=openai_api_key,
        verbose=True,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )

    # st.code(prompt)
    response = chat(prompt)

    return response


def parse_response(response, parser):
    plan = parser.parse(response.content)
    return plan


def convert_to_dataframe(plan):
    weeks, notes = plan.weeks, plan.notes

    workout_data = []
    for week in weeks:
        week_range, days = week.week_range, week.days
        for day in days:
            for exercise in day.exercises:
                row = {
                    "Week Range": week_range,
                    "Day Number": day.day_number,
                    "Focus": day.focus,
                    "Exercise Name": exercise.name,
                    # "Exercise Type": exercise.exercise_type,
                    "Sets": exercise.sets,
                    "Reps": exercise.reps,
                    "Duration": f"{exercise.duration.value} {exercise.duration.unit}"
                    if exercise.duration
                    else None,
                }
                workout_data.append(row)

    note_data = []
    for note in notes:
        row = {"note": note.content}
        note_data.append(row)

    return workout_data, note_data
