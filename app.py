import streamlit as st
import utils

st.set_page_config(page_title="FitAI", page_icon="🤖", layout="wide")
st.title("FitAI - Your AI fitness trainer")

st.subheader("Answer a few questions and get a tailored workout plan in ~5 minutes")


questions_list = utils.load_questions()
parser = utils.generate_parser()

answers = []
col1, col2 = st.columns(2)

with col1:
    for q in questions_list:
        answers.append(utils.generate_question_answer(q))

with col2:
    st.write(answers)
    submit_btn = st.button(
        "Generate plan!",
        key="submit",
        type="primary",
        use_container_width=True,
    )

    if submit_btn:
        messages = utils.generate_prompt(
            questions_list=questions_list,
            answers=answers,
            format_instructions=parser.get_format_instructions(),
        )

        response, plan, parsed = st.tabs(["Response", "Plan", "Parsed"])

        try:
            with st.spinner("Querying..."):
                with response:
                    response = utils.call_gpt(prompt=messages)
                    st.write(response)

                with plan:
                    plan = utils.parse_response(response=response, parser=parser)
                    st.write(plan)

                with parsed:
                    utils.print_plan(plan=plan)

        except Exception as e:
            st.exception(e)
