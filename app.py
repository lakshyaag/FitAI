import streamlit as st
import utils

st.set_page_config(page_title="FitAI", page_icon="💪", layout="wide")
st.title("💪 FitAI - Your AI fitness trainer")

st.subheader("Answer a few questions and get a tailored workout plan in ~5 minutes")

models = {
    "gpt-3.5-turbo": "GPT-3.5 (faster, but inaccurate)",
    "gpt-4": "GPT-4 (slower, but detailed)",
}

questions_list = utils.load_questions()
parser = utils.generate_parser()

answers = []
col1, col2 = st.columns(2)

with col1:
    sections = utils.get_sections(questions_list=questions_list)
    for s in sections:
        with st.expander(f"**{s}**"):
            for q in questions_list:
                if q["section"] == s:
                    answers.append(utils.generate_question_box(q))

    model = st.selectbox(
        "Choose model to use: ",
        options=models,
        index=0,
        format_func=lambda x: models[x],
    )

    submit_btn = st.button(
        "Generate plan!",
        key="submit",
        type="primary",
        use_container_width=True,
    )

with col2:
    st.info(
        (
            "Please note that the app may hang or run into an error. "
            "In such cases, try running the request again!"
        ),
        icon="🔔",
    )

    if submit_btn:
        messages = utils.generate_prompt(
            questions_list=questions_list,
            answers=answers,
            format_instructions=parser.get_format_instructions(),
        )

        try:
            with st.spinner(
                "💭 Building a personalized plan... this may take a few moments"
            ):
                response = utils.call_gpt(prompt=messages, model=model)

                plan = utils.parse_response(response=response, parser=parser)

                workout, notes = utils.convert_to_dataframe(plan=plan)

                workout_tab, notes_tab = st.tabs(["💪 Workouts", "📝 Notes"])

                with workout_tab:
                    st.dataframe(workout, use_container_width=True)
                with notes_tab:
                    st.dataframe(notes, use_container_width=True)

        except Exception as e:
            st.exception(e)
