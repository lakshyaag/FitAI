from langchain.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

STEPS_SCHEMA = """
Steps:
  summary: Summary of the CLIENT's answers
  steps:
    - step: Current step to be taken to generate a personalized workout plan for the CLIENT
"""  # noqa: E501

WORKOUT_SCHEMA = """
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
    - wk_range: Week 1-3
      days:
        - num: 1
          focus: Body Part A
          exs:
            - name: Exercise A1
              type: Type A
              sets: 3
              reps: 10
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
    template="""Your task is to act as a personal fitness trainer for a CLIENT. 
    You will be provided with information about your CLIENT's personal information, their fitness history, their goals, and any physical constraints they may have. 
    You have to prepare a detailed workout plan for the CLIENT, including everything essential for physical fitness.
    You will interact with the CLIENT only once currently, so do not think of steps that will be taken in the future.
    Ensure that you STRICTLY adhere to the number of days and weeks the CLIENT is willing to do their workout."""  # noqa: E501
)

first_message = HumanMessagePromptTemplate.from_template(
    template="""You will now be given a series of questions with the CLIENT's answers."""  # noqa: E501
)

qa_message = HumanMessagePromptTemplate.from_template(
    template="""{question}
    CLIENT: {answer}"""
)


format_message = HumanMessagePromptTemplate.from_template(
    template="""Summarize the CLIENT's answers for yourself. 
    Then, think in detailed step by step way AS A FITNESS TRAINER with all the answers provided by the CLIENT to be sure we can create a highly personalized workout routine. 
    Provide only the necessary steps as part of the response. DO NOT create the workout plan yet."""  # noqa: E501
)

steps_schema_message = HumanMessagePromptTemplate.from_template(
    template="""The output should be formatted in a way that conforms to the given YAML schema below.
    {steps_schema}
    """  # noqa: E501
)

schema_message = HumanMessagePromptTemplate.from_template(
    template="""
The output should be formatted in a way that conforms to the given schema below. As an example, a valid response is: 
{example_response}

Here is the output schema:
```
{output_schema}
```

Generate a highly personalized workout plan in the provide format. DO NOT ADD OR REMOVE EXTRA INDENTATIONS.
"""  # noqa: E501
)

plan_generator_message = HumanMessagePromptTemplate.from_template(
    template="""You will now be provided with a summary of the CLIENT's information and the steps to be taken to create a highly personalized workout plan.
    
    ```
    SUMMARY:
    {summary_gpt_response}
    ```

    ```
    STEPS: 
    {steps_gpt_response}
    ```

    Generate a highly personalized workout plan for the CLIENT with ONLY the provided information."""  # noqa: E501
)
