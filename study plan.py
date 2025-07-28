import streamlit as st
import json
import re
from datetime import datetime, timedelta

# Function to simulate LLM response for study plan and flashcards
def simulate_llm_response(subject, topic, duration_weeks, days_per_week, learning_style):
    study_db = {
        "calculus": {
            "derivatives": {
                "topics": [
                    {"day": "Day 1", "topic": "Introduction to Derivatives", "hours": 1.5},
                    {"day": "Day 2", "topic": "Power Rule", "hours": 1.0},
                    {"day": "Day 3", "topic": "Product and Quotient Rules", "hours": 1.5},
                    {"day": "Day 4", "topic": "Chain Rule", "hours": 1.5}
                ],
                "flashcards": [
                    {"question": "What is the derivative of x^2?", "answer": "2x"},
                    {"question": "What is the product rule?", "answer": "(f * g)' = f' * g + f * g'"},
                    {"question": "What is the chain rule?", "answer": "(f(g(x)))' = f'(g(x)) * g'(x)"}
                ]
            }
        }
    }

    topics = study_db.get(subject, {}).get(topic, {}).get("topics", [])[:days_per_week]
    flashcards = study_db.get(subject, {}).get(topic, {}).get("flashcards", [])

    plan = {}
    start_date = datetime.now()
    for week in range(duration_weeks):
        for i, topic_data in enumerate(topics):
            day = (start_date + timedelta(days=i + week * 7)).strftime("%Y-%m-%d")
            plan[day] = topic_data

    return {"study_plan": plan, "flashcards": flashcards}

# Streamlit app
st.title("Study Plan Generator")

# User input
subject = st.selectbox("Select Subject", ["calculus"])
topic = st.selectbox("Select Topic", ["derivatives"])
duration_weeks = st.slider("Duration (weeks)", 1, 4, 2)
days_per_week = st.slider("Days per week", 1, 7, 3)
learning_style = st.selectbox("Learning Style", ["visual", "textual"])

# Generate study plan
plan = simulate_llm_response(subject, topic, duration_weeks, days_per_week, learning_style)

# Display study plan
st.subheader("Study Plan")
if plan["study_plan"]:
    for day, details in plan["study_plan"].items():
        st.write(f"📅 {day}: **{details['topic']}** ({details['hours']} hours)")
else:
    st.error("No study plan available.")

# Display flashcards
st.subheader("Flashcards")
if plan["flashcards"]:
    for flashcard in plan["flashcards"]:
        with st.expander(flashcard["question"]):
            st.write(f"✅ **Answer:** {flashcard['answer']}")
else:
    st.error("No flashcards available.")