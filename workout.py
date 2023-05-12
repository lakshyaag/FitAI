from typing import List
from pydantic import BaseModel, Field


class Duration(BaseModel):
    value: int = Field(
        description="Numerical value representing the duration of the exercise"
    )
    unit: str = Field(
        description="Unit of time for the duration (e.g., seconds, minutes)"
    )


class Exercise(BaseModel):
    name: str = Field(description="Specific exercise to perform in the workout plan")
    # exercise_type: str = Field(
    #     description="Category of the exercise (e.g., warmup, cardio, strength)"
    # )
    sets: int = Field(description="Total number of sets of the exercise to complete")
    reps: int = Field(
        description="Total number of repetitions of the exercise in each set"
    )
    duration: Duration = Field(
        default=None, description="Duration of the exercise, if applicable"
    )


class Day(BaseModel):
    day_number: int = Field(
        description="Sequential number of the day in the workout plan"
    )
    focus: str = Field(
        description="Primary muscle group or activity targeted on that day"
    )
    exercises: List[Exercise] = Field(
        description="Sequence of exercises to perform on the day"
    )


class Week(BaseModel):
    week_range: str = Field(
        description=(
            "Identifies the specific week or range of weeks this plan covers"
            " (e.g., Week 1-2)"
        )
    )
    days: List[Day] = Field(
        description=(
            "Ordered list of daily workout plans, each containing exercises and"
            "focus areas for the given week"
        )
    )


class Note(BaseModel):
    content: str = Field(description="The content of the note")


class WorkoutPlan(BaseModel):
    weeks: List[Week] = Field(
        description=(
            "Organized series of weekly workout plans, "
            "creating a comprehensive and structured fitness program"
        )
    )
    notes: List[Note] = Field(
        description=(
            "Supplementary information, tips or instructions "
            "to support and enhance the overall workout plan"
        )
    )
