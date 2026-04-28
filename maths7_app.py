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

# Logo + Title
st.image("logo.png", width=120)
st.title("Smart7 Maths Practice App")

# Compact Splash Section
st.markdown("""
<div style="background-color:#f0f8ff; padding:15px; border-radius:8px; margin-bottom:20px;">
    <h3>📖 About Smart7</h3>
    <p>Smart7 helps Grade 7 learners build confidence in <b>fractions, algebra, geometry, and word problems</b>.</p>
    <p>Learners get <b>instant feedback</b>, <b>progress tracking</b>, and <b>motivational achievements</b> — making maths less intimidating and more fun.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls for Demo vs Full Mode
st.sidebar.header("Smart7 Modes")

# Mode selection
mode = st.sidebar.radio(
    "Choose mode:",
    ["Demo (10 questions)", "Full (100 questions)"],
    index=0
)

# If Demo Mode, limit questions
if mode == "Demo (10 questions)":
    questions = questions[:10]

# Unlock Full Mode via Yoco
st.sidebar.markdown("---")
st.sidebar.subheader("Unlock Full Mode")
st.sidebar.write("To access all 100 questions, please unlock Full Mode below:")

if st.sidebar.button("🔓 Unlock via Yoco"):
    st.sidebar.success("Redirecting to Yoco payment...")
    st.sidebar.markdown("[Click here to pay](https://pay.yoco.com/your-link)")
    # Replace with your actual Yoco checkout link

# Custom CSS for Start + Submit + Next buttons
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
    # Progress tracker
    st.subheader(f"Question {st.session_state.index+1} of {len(questions)}")
    st.progress((st.session_state.index+1) / len(questions))

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
