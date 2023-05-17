import json
import os

import streamlit as st
import yaml
from dotenv import find_dotenv, load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from prompts import (
    EXAMPLE_RESPONSE,
    WORKOUT_SCHEMA,
    STEPS_SCHEMA,
    first_message,
    format_message,
    qa_message,
    plan_generator_message,
    schema_message,
    steps_schema_message,
    system_message,
)
from workout import WorkoutPlan

load_dotenv(find_dotenv())

openai_api_key = os.environ.get("OPENAI_API_KEY")


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
    elif question["question_type"] == "multi_select":
        answer_choices = question["options"]
        return st.multiselect(
            label=f"**{question_text}**", options=answer_choices, key=question["id"]
        )
    elif question["question_type"] == "numeric_input":
        return st.number_input(
            label=f"**{question_text}**",
            min_value=0.00,
            value=50.00,
            key=question["id"],
        )
    elif question["question_type"] == "text_input":
        return st.text_input(
            label=f"**{question_text}**", key=question["id"], value="N/A"
        )


@st.cache_data()
def generate_qa_messages(questions_list, answers):
    qa_messages = [
        qa_message.format(question=q["text"], answer=answers[(q["id"])])
        for q in questions_list
    ]
    return qa_messages


def parse_summary_steps_response(summary_steps_response):
    summary_steps_yaml = yaml.safe_load(summary_steps_response.content)["Steps"]

    return summary_steps_yaml


def generate_steps_prompt(qa_messages):
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message,
            first_message,
            format_message,
            steps_schema_message,
        ]
    )

    messages = chat_prompt.format_prompt(
        steps_schema=STEPS_SCHEMA,
    ).to_messages()

    for x in reversed(qa_messages):
        messages.insert(1, x)

    return messages


def generate_workout_prompt(summary_steps_yaml):
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message, plan_generator_message, schema_message]
    )

    summary_gpt_response = yaml.safe_dump(summary_steps_yaml["summary"])
    steps_gpt_response = yaml.safe_dump(summary_steps_yaml["steps"])

    messages = chat_prompt.format_prompt(
        output_schema=WORKOUT_SCHEMA,
        example_response=EXAMPLE_RESPONSE,
        summary_gpt_response=summary_gpt_response,
        steps_gpt_response=steps_gpt_response,
    ).to_messages()

    return messages


def call_gpt(prompt, model="gpt-4"):
    chat = ChatOpenAI(
        model_name=model,
        temperature=0.1,
        openai_api_key=openai_api_key,
        verbose=True,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )

    # st.write(chat.get_num_tokens_from_messages(prompt))
    # st.write(prompt)
    response = chat(prompt)

    return response


def parse_response(response):
    response_json = yaml.safe_load(response.content)

    # with open("response.json", "w") as f:
    #     json.dump(response_json, f)

    plan = WorkoutPlan(**response_json["WorkoutPlan"])
    return plan


def convert_to_dataframe(plan):
    weeks, notes = plan.wks, plan.notes

    workout_data = []
    for week in weeks:
        week_range, days = week.wk_range, week.days
        for day in days:
            if day.exs:
                for exercise in day.exs:
                    row = {
                        "Week Range": week_range,
                        "Day Number": day.num,
                        "Focus": day.focus,
                        "Exercise Name": exercise.name,
                        "Exercise Type": exercise.type,
                        "Sets": exercise.sets,
                        "Reps": exercise.reps,
                        "Duration": f"{exercise.dur.val} {exercise.dur.unit}"
                        if exercise.dur
                        else None,
                    }
                    workout_data.append(row)
            else:
                row = {
                    "Week Range": week_range,
                    "Day Number": day.num,
                    "Focus": day.focus,
                    "Exercise Name": None,
                    "Exercise Type": None,
                    "Sets": None,
                    "Reps": None,
                    "Duration": None,
                }
                workout_data.append(row)

    note_data = []
    for note in notes:
        row = {"note": note.content}
        note_data.append(row)

    return workout_data, note_data
