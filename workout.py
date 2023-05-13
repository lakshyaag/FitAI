from typing import List, Optional
from pydantic import BaseModel, Field


class D(BaseModel):
    val: int
    unit: str


class Ex(BaseModel):
    name: str
    type: str
    sets: str = Field(default=None)
    reps: str = Field(default=None)
    dur: Optional[D] = Field(default=None)


class Day(BaseModel):
    num: int
    focus: str
    exs: Optional[List[Ex]]


class Wk(BaseModel):
    wk_range: str
    days: List[Day]


class N(BaseModel):
    content: str


class WorkoutPlan(BaseModel):
    wks: List[Wk]
    notes: List[N]
