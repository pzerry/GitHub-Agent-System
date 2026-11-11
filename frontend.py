import requests
import streamlit as st


st.title("GitHub AI Assistant")

with st.form("question_form"):
    question = st.text_input(
        "Ask about a GitHub repository",
        placeholder="Show recent commits for owner/repo",
    )
    submitted = st.form_submit_button("Ask")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Getting your answer..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"question": question.strip()},
                    timeout=120,
                )

                response.raise_for_status()
                data = response.json()

                st.write(data["answer"])

            except requests.RequestException as error:
                st.error(f"Request failed: {error}")