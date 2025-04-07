import json, re
import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def render_profile():
    # Two-column layout
    col1, col2 = st.columns(2)

    # 🧍‍♀️ Column 1: User Profile
    with col1:
        st.subheader("👤 User Profile")
        age = st.number_input("Age", min_value=5, max_value=100, value=25)
        sex = st.selectbox("Sex", ["Female", "Male", "Other"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=165)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=60)
        injuries = st.text_input("Physical conditions or injuries (optional)", placeholder="e.g., Back pain, Knee issues")

    # 🧘‍♀️ Column 2: Yoga Preferences
    with col2:
        st.subheader("🧘‍♀️ Yoga Preferences")
        goals = st.multiselect(
            "Primary yoga goals",
            ["Flexibility", "Strength", "Relaxation / Stress relief", "Weight loss", "Balance and posture improvement", "General well-being"]
        )

        experience = st.selectbox(
            "Yoga experience level",
            ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
        )

        duration = st.selectbox(
            "Preferred session duration",
            ["10–15 minutes", "20–30 minutes", "30–45 minutes", "1 hour or more"]
        )

        time_of_day = st.selectbox(
            "Preferred time of day for practice",
            ["Morning", "Afternoon", "Evening", "Flexible / No preference"]
        )

        pace = st.selectbox(
            "Preferred session pace",
            ["Slow and calming (Yin, Restorative)", "Moderate and flowing (Hatha, Vinyasa)", "Fast and energizing (Power Yoga)", "Not sure"]
        )
    
    # Construct a profile summary string to display
    profile = f"""
    **Basic Info:**
    - Age: {age}
    - Height: {height} cm
    - Weight: {weight} kg

    **Lifestyle & Yoga Goals:**
    - Sex: {sex}
    - Experience Level: {experience}
    - Yoga Goals: {', '.join(goals) if goals else 'Not specified'}
    - Preferred Duration: {duration}
    - Preferred Time of Day: {time_of_day}
    - Preferred Pace: {pace}

    **Additional Details:**
    - Physical Conditions or Injuries: {injuries if injuries.strip() else 'None'}
    """

    return profile 

def initialize_openai_model():
    try:
        api_key = st.session_state.openai_api_key
        return OpenAIChat(id='gpt-4o', api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error initializing OpenAI Model: {e}")
        return None

def extract_json_from_string(text: str) -> dict:
    # Split the text into lines
    lines = text.splitlines()
    # Filter out lines that start with the code fence (``` or ```json)
    json_lines = [line for line in lines if not line.strip().startswith("```")]
    # Join the remaining lines back into a single string
    json_str = "\n".join(json_lines)
    # Parse the JSON string into a dictionary
    return json.loads(json_str)

def generate_yoga_plan(openai_model, user_profile: str) -> dict:
    """
    Generate a personalized yoga plan based on the user's profile.

    The agent is instructed to return a valid JSON object with the following keys:
      - sequence_overview
      - poses_and_durations
      - modifications_and_alternatives
      - recommendations
      - wellness_tips

    Each value should be a plain string that may include markdown formatting and multiple lines.
    """

    # Map duration in profile to number of poses
    duration_to_pose_count = {
        "10–15 minutes": 8,
        "20–30 minutes": 12,
        "30–45 minutes": 16,
        "1 hour or more": 20
    }

    # Get the correct number of poses based on user's duration
    num_poses = next(
        (count for duration, count in duration_to_pose_count.items() if duration in user_profile),
        8  # default fallback
    )

    yoga_agent = Agent(
        name="Yoga Planner",
        role="Provides personalized yoga routines and wellness recommendations",
        model=openai_model,
        instructions = [
            "Consider the user's profile, including their experience level, personal goals, and any physical limitations.",
            "Generate a comprehensive yoga plan that includes the following sections: sequence overview, pose sequence, modifications, recommendations, and wellness tips. Do NOT include headings like 'Sequence Overview:' or 'Modifications:' in the text itself. Instead, just provide the text for each section.",
            "Include a section for Sequence Overview that describes the style of yoga and what the session is designed to achieve.",
            f"Include a section for Poses and Durations that contains exactly **{num_poses} yoga poses**. Each pose should follow this format: use a subheading (###) with the English name and Sanskrit name in parentheses. Under each heading, write exactly **three sentences** explaining how to perform the pose. After that, include a separate line with the recommended duration or number of breaths, formatted in bold like '**Duration:** 5 breaths' or '**Hold:** 30 seconds'. Ensure the formatting is clean and uses markdown.",
            "Example formatting:\n\n### Cat-Cow Pose (Marjaryasana-Bitilasana)\nStart on all fours with wrists under shoulders and knees under hips. Inhale to arch the back and look up (Cow). Exhale to round the spine and tuck the chin (Cat).\n**Duration:** 5 rounds (2–3 breaths per round)",
            "Include a section for Modifications and Alternatives that offers safe substitutions or adjustments for beginners or users with injuries. Use markdown formatting to organize the tips clearly.",
            "Include a section for Recommendations that outlines how often the user should practice this sequence, ideal times of day, and any complementary activities. Use markdown bullet points for clarity.",
            "Include a section for Wellness Tips that provides general suggestions related to hydration, environment setup, and staying consistent with practice. Use markdown bullet points for clarity.",
            "Return your response as a valid JSON object with the keys: 'sequence_overview', 'poses_and_durations', 'modifications_and_alternatives', 'recommendations', and 'wellness_tips'.",
            "Each value must be a plain string (single-depth) that can include multiple lines and markdown formatting, with no nested objects."
        ]
    )

    response = yoga_agent.run(user_profile)

    try:
        plan = extract_json_from_string(response.content)
    except Exception as e:
        st.error(f"Failed to parse JSON response: {e}")
        plan = {
            "sequence_overview": "Not available",
            "poses_and_durations": "Not available",
            "modifications_and_alternatives": "Not available",
            "recommendations": "Not provided",
            "wellness_tips": "Not provided"
        }

    return plan

def display_yoga_plan(plan: dict):
    """
    Display the personalized yoga plan in a well-structured and visually appealing format.
    """

    st.markdown("## 🧘‍♀️ Your Personalized Yoga Plan")

    st.markdown("---")
    st.markdown("## 🧩 Sequence Overview")
    st.markdown(plan.get("sequence_overview", "_No overview available._"))

    st.markdown("---")
    st.markdown("## 📋 Pose Sequence")

    pose_text = plan.get("poses_and_durations", "")
    if pose_text:
        # Split into pose blocks using subheadings (### ...)
        pose_blocks = re.split(r'(?=^### )', pose_text, flags=re.MULTILINE)
        pose_blocks = [block.strip() for block in pose_blocks if block.strip()]

        # Update each block with sequence number and ensure duration is on a new line
        numbered_blocks = []
        for idx, block in enumerate(pose_blocks):
            # Add numbering to heading (### Pose Name...)
            block = re.sub(r'^###\s+(.*)', f"### {idx + 1}. \\1", block)

            # Move any bolded duration/hold line to a new line
            block = re.sub(r'(\*\*(Duration|Hold):.*?\*\*)', r'\n\1', block)

            numbered_blocks.append(block)

        # Display blocks 4 per row
        for i in range(0, len(numbered_blocks), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i + j < len(numbered_blocks):
                    with col:
                        st.markdown(numbered_blocks[i + j])
    else:
        st.markdown("_No pose sequence available._")

    st.markdown("---")


    st.markdown("## 🔄 Modifications & Alternatives")
    st.markdown(plan.get("modifications_and_alternatives", "_No modifications available._"))
    st.markdown("---")

    st.markdown("## 🗓️ Practice Recommendations")
    st.markdown(plan.get("recommendations", "_No recommendations provided._"))
    st.markdown("---")

    st.markdown("## 🌿 Wellness Tips")
    st.markdown(plan.get("wellness_tips", "_No tips available._"))
    st.markdown("---")
    
def main() -> None:
    # Page config
    st.set_page_config(page_title="Yoga Planner Bot", page_icon="🧘‍♀️", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🧘‍♀️ Yoga Planner Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Yoga Planner Bot — a smart Streamlit application that curates personalized yoga routines based on your goals, experience, and daily lifestyle to help you build a mindful and consistent practice.",
        unsafe_allow_html=True
    )

    # Get OpenAI API Key
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )

    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.success("✅ API key updated!")

    st.markdown("---")

    user_profile = render_profile()
    st.markdown("---")

    # Generate button
    if st.button("🧘‍♀️ Generate My Personalized Yoga Plan"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key.")
        else:
            openai_model = initialize_openai_model()
            with st.spinner("Creating your customized Yoga Plan ..."):
                yoga_plan = generate_yoga_plan(openai_model, user_profile)
                st.session_state.yoga_plan = yoga_plan  # Store in session state

    # Render yoga plan if available in session state
    if "yoga_plan" in st.session_state:
        yoga_plan = st.session_state.yoga_plan

        display_yoga_plan(yoga_plan)

        # Disclaimer
        st.markdown(
            "⚠️ **Disclaimer:** This yoga plan is AI-generated and is intended for general wellness. "
            "Please consult a certified yoga instructor or healthcare professional before beginning any new exercise routine."
        )

        # Combine plan into downloadable string
        full_plan_text = "\n\n".join([
            "🧩 Sequence Overview\n" + yoga_plan.get("sequence_overview", ""),
            "📋 Pose Sequence\n" + yoga_plan.get("poses_and_durations", ""),
            "🔄 Modifications & Alternatives\n" + yoga_plan.get("modifications_and_alternatives", ""),
            "🗓️ Practice Recommendations\n" + yoga_plan.get("recommendations", ""),
            "🌿 Wellness Tips\n" + yoga_plan.get("wellness_tips", "")
        ])

        st.download_button(
            label="📥 Download Yoga Plan",
            data=full_plan_text,
            file_name="yoga_plan.txt",
            mime="text/plain"
        )


if __name__ == "__main__": 
    main()