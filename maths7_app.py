import json
import streamlit as st

# Load questions from JSON
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.show_feedback = False
    st.session_state.last_correct = None
if "full_unlocked" not in st.session_state:
    st.session_state.full_unlocked = False

# Logo + Title
st.image("logo.png", width=120)
st.title("Smart7 Maths Practice App")

# Learner-friendly splash with extra explanation
st.markdown("""
<div style="background-color:#e6ffe6; padding:12px; border-radius:8px; margin-bottom:20px;">
    <h4>🎓 Welcome to Smart7!</h4>
    <p>Smart7 helps Grade 7 learners practice <b>fractions, algebra, geometry, and word problems</b> with confidence.</p>
    <p>Start with <b>Demo Mode</b> (10 free questions) to see how the app works.</p>
    <p>Parents can unlock <b>Full Mode</b> (100 questions) using secure Yoco payment.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("Smart7 Modes")

# Default: Demo Mode
mode = "Demo (10 questions)"
questions = questions[:10]

# Unlock Full Mode via Yoco
st.sidebar.markdown("---")
st.sidebar.subheader("Unlock Full Mode")
st.sidebar.write("Parents can unlock all 100 questions below:")

# ✅ Real Yoco payment link
st.sidebar.markdown("[Click here to pay securely via Yoco](https://pay.yoco.com/r/2PeKx1)")

# Manual confirmation after payment
if st.sidebar.checkbox("✅ I have completed payment"):
    st.session_state.full_unlocked = True

# If unlocked, enable Full Mode
if st.session_state.full_unlocked:
    mode = "Full (100 questions)"
    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    st.sidebar.success("✅ Full Mode unlocked — your child now has access to all 100 questions 🎉")

# Custom CSS for buttons
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: green;
        color: white;
        font-weight: bold;
    }
    div.stButton > button:contains('Submit') {
        background-color: green;
        color: white;
        font-weight: bold;
    }
    div.stButton > button:contains('Next') {
        background-color: blue;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Start screen
if not st.session_state.started:
    st.subheader("Welcome to Smart7!")
    st.write("This app contains 100 Grade 7 maths questions. Click below to begin.")
    if st.button("Start Practice"):
        st.session_state.started = True
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()

else:
    # Progress tracker with fix
    progress_value = min((st.session_state.index+1) / len(questions), 1.0)
    st.subheader(f"Question {st.session_state.index+1} of {len(questions)}")
    st.progress(progress_value)

    # If quiz finished
    if st.session_state.index >= len(questions):
        st.subheader("🎉 Summary")
        st.write(f"Score: {st.session_state.score}/{len(questions)}")
        percent = (st.session_state.score / len(questions)) * 100
        st.write(f"Percentage: {percent:.1f}%")

        if percent >= 80:
            st.success("🌟 Gold Achievement")
        elif percent >= 60:
            st.info("🥈 Silver Achievement")
        elif percent >= 40:
            st.warning("🥉 Bronze Achievement")
        else:
            st.error("💡 Keep practicing!")

        if st.button("Reset Quiz"):
            st.session_state.started = False
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.show_feedback = False
            st.rerun()

    else:
        # Current question
        q = questions[st.session_state.index]
        st.subheader(q['question'])
        choice = st.radio("Choose an answer:", q["options"], key=st.session_state.index)

        if st.button("Submit"):
            if choice == q["answer"]:
                st.session_state.last_correct = True
                st.session_state.score += 1
            else:
                st.session_state.last_correct = False
            st.session_state.show_feedback = True

        if st.session_state.show_feedback:
            if st.session_state.last_correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. {q['explanation']}")

        # Navigation
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Previous") and st.session_state.index > 0:
                st.session_state.index -= 1
                st.session_state.show_feedback = False
                st.rerun()
        with col2:
            if st.button("Next"):
                st.session_state.index += 1
                st.session_state.show_feedback = False
                st.rerun()
        with col3:
            if st.button("Back to Top"):
                st.session_state.index = 0
                st.session_state.show_feedback = False
                st.rerun()
        with col4:
            if st.button("Reset Quiz"):
                st.session_state.started = False
                st.session_state.index = 0
                st.session_state.score = 0
                st.session_state.show_feedback = False
                st.rerun()
