from langchain.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

SCHEMA = """
WorkoutPlan:
  wks:
    - wk_range: Week or range of weeks in the plan (e.g., Week 1-2).
    days:
      - num: Day number within the workout plan.
      - focus: Primary muscle group or activity targeted on this day.
      exs:
        - name: Name of the exercise.
        - type: Category of the exercise (warmup, cardio, stretching, or strength).
        - sets: Number of sets to perform.
        - reps: Number of repetitions per set.
        dur:
          val: Duration value of the exercise.
          unit: Time unit for the duration (e.g., seconds, minutes).
  notes:
    - content: Additional information, tips, or instructions related to the workout plan as individual items.
"""  # noqa: E501

EXAMPLE_RESPONSE = """
WorkoutPlan:
  wks:
    - wk_range: Week 1-2
      days:
        - num: 1
          focus: Body Part A
          exs:
            - name: Exercise A1
              type: Type A
              sets: 3
              reps: 10
            - name: Exercise A2
              type: Type C
              sets: 3
              reps: 12
            - name: Exercise A3
              type: Type B
              dur:
                val: 30
                unit: seconds
        - num: 2
          focus: Body Part B
          exs:
            - name: Exercise B1
              type: Type A
              sets: 4
              reps: 8
            - name: Exercise B2
              type: Type A
              sets: 3
              reps: 10
            - name: Exercise B3
              type: Type C
              dur:
                val: 1
                unit: minute
  notes:
    - content: Note 1
    - content: Note 2
"""

system_message = SystemMessagePromptTemplate.from_template(
    """Your task is to act as a personal fitness trainer. 
    You will be provided with information about your CLIENT's current fitness level, their goals, and other preferences they have. 
    You have to prepare a detailed workout plan for the CLIENT, including everything essential for physical fitness.
    Ensure that you strictly adhere to the number of days and weeks the CLIENT is willing to do their workout."""  # noqa: E501
)

first_message = HumanMessagePromptTemplate.from_template(
    template="""You will now be given a series of questions and answers containing information about the CLIENT
    """  # noqa: E501
)

qa_message = HumanMessagePromptTemplate.from_template(
    template="""{question}
    CLIENT: {answer}
    """
)


format_message = HumanMessagePromptTemplate.from_template(
    template="""With the given details, proceed to create a detailed weekly plan that can be followed for 2 months for the CLIENT, making sure to incorporate their inputs properly. 
Ensure that you include cardio and rest time inside the plan as part of the `exercise` object.  If a day is classified as "rest day", skip it from your output. 
Try to keep the notes section as generic as possible as most CLIENTS will not read it."""  # noqa: E501
)


schema_message = HumanMessagePromptTemplate.from_template(
    template="""
The output should be formatted in a way that conforms to the given schema below. As an example, a valid response is: 
{example_response}

Here is the output schema:
```
{output_schema}
```
"""  # noqa: E501
)
