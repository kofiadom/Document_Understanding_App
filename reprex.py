### I isolated the feedback section to investigate what was causing the problem
### To check whether the radio buttons disappear after clicking on an option

import streamlit as st
import json
from datetime import datetime

def save_feedback(feedback_option, context):
    """Save feedback to a JSON file."""
    feedback_data = {
        "timestamp": datetime.now().isoformat(),
        "feedback_option": feedback_option, 
        "context": context,
    }

    try:
        # Attempt to read existing feedback data
        with open('feedback_data.json', 'r+') as f:
            try: 
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            data.append(feedback_data)
            f.seek(0) 
            json.dump(data, f, indent=2)

    except FileNotFoundError:
        # Create a new file if it doesn't exist
        with open('feedback_data.json', 'w') as f:
            json.dump([feedback_data], f, indent=2)

def collect_feedback():
    """Simplified feedback function for reprex."""

    feedback_key = "feedback" 

    if feedback_key not in st.session_state:
        st.session_state[feedback_key] = {"feedback_option": None, "context": ""}

    st.write("Was this response helpful?")

    # Use variables to store values from session state
    feedback_option = st.session_state[feedback_key]["feedback_option"]
    context = st.session_state[feedback_key]["context"]

    # Radio button for feedback selection
    feedback_option = st.radio(
        "Select Feedback",
        options=["👍 Yes, it was helpful", "👎 No, it could be improved"],
        key=None, 
    )

    # Update session state after the radio button is rendered
    st.session_state[feedback_key]["feedback_option"] = feedback_option

    # Conditional text input 
    if st.session_state[feedback_key]["feedback_option"] == "👎 No, it could be improved": 
        context = st.text_input("What could be improved?", key=None)
        st.session_state[feedback_key]["context"] = context 

    # Button to submit feedback (Simplified for reprex)
    if st.button("Submit Feedback"):
        feedback_option = st.session_state[feedback_key]["feedback_option"]
        context = st.session_state[feedback_key]["context"]
        st.write("Feedback Option (On Submit):", feedback_option) 
        st.write("Context (On Submit):", context)

        save_feedback(feedback_option, context)
        st.success("Thank you for your feedback!") 


collect_feedback()