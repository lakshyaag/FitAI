from typing import List
from pydantic import BaseModel, Field


class Duration(BaseModel):
    value: int = Field(description="numerical value of a duration")
    unit: str = Field(description="the unit of time of a duration")


class Exercise(BaseModel):
    name: str = Field(description="name of the exercise")
    exercise_type: str = Field(
        default=None,
        description="type of exercise (e.g., warmup, cardio, stretching, strength)",
    )
    sets: int = Field(default=None, description="number of sets to perform")
    reps: int = Field(default=None, description="number of repetitions per set")
    duration: Duration = Field(
        default=None, description="duration of the exercise, if applicable"
    )


class Day(BaseModel):
    day_number: int = Field(description="the day number within the workout plan")
    focus: str = Field(description="primary focus area of the day")
    exercises: List[Exercise] = Field(
        default=None, description="list of exercises to be performed"
    )


class Week(BaseModel):
    week_range: str = Field(
        description="week numbers the workout plan has to be followed (e.g., Week 1-4, Week 5-7)"  # noqa: E501
    )
    days: List[Day] = Field("list of days in the workout plan for specific week")


class Note(BaseModel):
    content: str = Field(description="the content of the note")


class WorkoutPlan(BaseModel):
    weeks: List[Week] = Field("list of weeks in the workout plan")
    notes: List[Note] = Field("list of notes for the workout plan")
