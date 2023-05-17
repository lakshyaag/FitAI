import streamlit as st
import streamlit_utils as utils

st.set_page_config(page_title="FitAI", page_icon="💪", layout="wide")
st.title("💪 FitAI - Your AI fitness trainer")

st.subheader("Answer a few questions and get a tailored workout plan in ~5 minutes")

models = {
    "gpt-3.5-turbo": "GPT-3.5 (faster, but inaccurate and error-prone)",
    "gpt-4": "GPT-4 (slower, but detailed)",
}

questions_list = utils.load_questions()

answers = {}
col1, col2 = st.columns([1, 2])

with col1:
    sections = utils.get_sections(questions_list=questions_list)
    for s in sections:
        with st.expander(f"**{s}**"):
            for q in questions_list:
                if q["section"] == s:
                    answers[q["id"]] = utils.generate_question_box(q)

    model = st.selectbox(
        "Choose model to use: ",
        options=models,
        index=1,
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
        # st.write(answers)
        qa_messages = utils.generate_qa_messages(
            questions_list=questions_list, answers=answers
        )

        steps_messages = utils.generate_steps_prompt(qa_messages=qa_messages)

        try:
            tab_summary, tab_workout, tab_notes = st.tabs(
                ["💡 Summary", "💪 Workout", "📝 Notes"]
            )
            with tab_summary:
                with st.spinner("💭 Summarizing your information..."):
                    summary_steps_response = utils.call_gpt(
                        prompt=steps_messages, model="gpt-3.5-turbo"
                    )

                    summary_steps_yaml = utils.parse_summary_steps_response(
                        summary_steps_response=summary_steps_response
                    )

                    st.subheader("Summary")
                    st.write(summary_steps_yaml["summary"])

                    st.subheader("Steps")
                    st.write(summary_steps_yaml["steps"])

                with tab_workout:
                    with st.spinner("☕ Generating your personalized workout plan..."):
                        workout_messages = utils.generate_workout_prompt(
                            summary_steps_yaml=summary_steps_yaml
                        )
                        response = utils.call_gpt(prompt=workout_messages, model=model)

                        plan = utils.parse_response(response=response)

                        workout, notes = utils.convert_to_dataframe(plan=plan)
                        st.dataframe(workout, use_container_width=True)
                with tab_notes:
                    st.dataframe(notes, use_container_width=True)

        except Exception as e:
            st.exception(e)
