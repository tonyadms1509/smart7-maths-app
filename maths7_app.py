import streamlit as st
import random
import json

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)


st.title("Smart7 Maths Practice App")

# Splash page
if "quiz_started" not in st.session_state:
    st.markdown("## 🚀 Welcome to Smart7\nClick Start to begin your Grade 7 maths practice quiz.")
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.finished = False

# Quiz flow
if st.session_state.get("quiz_started") and not st.session_state.get("finished"):
    q_index = st.session_state.current_q
    q = questions[q_index]

    st.write(f"**Question {q_index+1}: {q['question']}**")
    choice = st.radio("Select your answer:", q["options"], key=f"q{q_index}")

    if st.button("Submit Answer"):
        st.session_state.answers[q_index] = choice
        if choice == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")
        if q.get("explanation"):
            st.info(q["explanation"])

    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Previous") and q_index > 0:
            st.session_state.current_q -= 1
    with col2:
        if st.button("Next") and q_index < len(questions)-1:
            st.session_state.current_q += 1
    with col3:
        if st.button("Reset Quiz"):
            st.session_state.quiz_started = False
    with col4:
        if st.button("Finish Quiz"):
            st.session_state.finished = True

    st.progress((q_index+1)/len(questions))
    st.write(f"Question {q_index+1} of {len(questions)}")

# Results
if st.session_state.get("finished"):
    correct = sum(1 for i,q in enumerate(questions) if st.session_state.answers.get(i) == q["answer"])
    total = len(questions)
    percent = (correct/total)*100
    st.success(f"🎉 Finished! Score: {correct}/{total} ({percent:.1f}%)")
