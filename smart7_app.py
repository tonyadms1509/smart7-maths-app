import streamlit as st
import json
import random

# --- Splash Screen ---
st.image("logo.png", use_column_width=True)
st.title("Smart7 Maths Practice App")
st.markdown("**Building confidence, one question at a time.**")

# --- Mode Selection ---
st.sidebar.header("Mode Selection")
mode = st.sidebar.radio("Choose a mode:", ["Demo Mode (10 Questions)", "Full Mode (100 Questions)"])

# --- Payment Unlock ---
if mode == "Full Mode (100 Questions)":
    st.sidebar.markdown("To unlock Full Mode, please complete payment:")
    st.sidebar.markdown("[Pay with Yoco](https://pay.yoco.com/r/2PeKx1)")
    payment_done = st.sidebar.checkbox("I have completed payment ✅")
else:
    payment_done = False

# --- Load Questions ---
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

if mode == "Demo Mode (10 Questions)":
    questions = random.sample(all_questions, 10)
elif mode == "Full Mode (100 Questions)" and payment_done:
    questions = all_questions
else:
    questions = []

# --- Progress + Navigation ---
if questions:
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    current_index = st.session_state.current_index
    st.progress((current_index+1)/len(questions))

    q = questions[current_index]
    st.subheader(f"Question {current_index+1}: {q['question']}")
    choice = st.radio("Choose an answer:", q["options"], key=current_index)

    if st.button("Submit"):
        if choice == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: {q['answer']}")
        st.info(q["explanation"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Previous") and current_index > 0:
            st.session_state.current_index -= 1
            st.experimental_rerun()
    with col2:
        if st.button("Next") and current_index < len(questions)-1:
            st.session_state.current_index += 1
            st.experimental_rerun()
    with col3:
        if st.button("Back to Top"):
            st.session_state.current_index = 0
            st.experimental_rerun()
    with col4:
        if st.button("Reset Quiz"):
            st.session_state.current_index = 0
            st.experimental_rerun()
else:
    if mode == "Full Mode (100 Questions)" and not payment_done:
        st.warning("Please complete payment via Yoco to unlock Full Mode.")
    else:
        st.info("Demo Mode ready — select it in the sidebar to begin.")
