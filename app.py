"""
Simple Streamlit UI for the Pediatric AI Health Companion.
"""
import streamlit as st
from data_models import ChildHealthProfile
from health_engine import generate_health_plan


def _format_key(key: str) -> str:
    """Turn camelCase or lowercase into Title Case (e.g. dailyWellnessPlan -> Daily Wellness Plan)."""
    if not key:
        return key
    out = []
    for i, c in enumerate(key):
        if c.isupper() and i and key[i - 1].isalpha():
            out.append(" ")
        out.append(c)
    return "".join(out).replace("_", " ").title()


def _value_to_markdown(value, level: int = 0) -> str:
    """Convert a JSON-like value to Markdown (headings and bullets)."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(_value_to_markdown(item, level + 1))
            else:
                lines.append(f"- {item}")
        return "\n".join(lines)
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            title = _format_key(k)
            if isinstance(v, dict):
                lines.append(f"\n**{title}**\n")
                lines.append(_value_to_markdown(v, level + 1))
            elif isinstance(v, list):
                lines.append(f"\n**{title}**\n")
                lines.append(_value_to_markdown(v, level + 1))
            elif isinstance(v, str) and v.strip():
                lines.append(f"- **{title}:** {v}")
            else:
                lines.append(f"- **{title}:** {v}")
        return "\n".join(lines).strip()
    return str(value)

st.set_page_config(
    page_title="Health is Wealth",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .main { max-width: 720px; margin: 0 auto; padding: 1rem; }
    h1 { color: #0e7490; font-weight: 600; }
    .stMetric { background: #f0fdfa; padding: 0.75rem; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🩺 Health is Wealth")
st.caption("Pediatric AI Health Companion — personalized wellness guidance for your child.")

with st.form("child_profile_form"):
    st.subheader("Child profile")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", placeholder="e.g. Aarav")
        age = st.number_input("Age (years)", min_value=1, max_value=18, value=10)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=220.0, value=138.0, step=0.5)
        weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=150.0, value=42.0, step=0.1)
    with col2:
        sleep_hours = st.number_input("Sleep (hours/night)", min_value=0.0, max_value=14.0, value=7.0, step=0.5)
        screen_time_hours = st.number_input("Screen time (hours/day)", min_value=0.0, max_value=24.0, value=4.0, step=0.5)
        physical_activity_level = st.selectbox(
            "Physical activity",
            ["Low", "Moderate", "High"],
        )
        eating_habits = st.text_area(
            "Eating habits",
            placeholder="e.g. Prefers junk food, low vegetables",
            height=80,
        )
        mood = st.text_input("Mood", placeholder="e.g. Often tired")
        symptoms = st.text_input("Symptoms (optional)", placeholder="e.g. Occasional headaches")

    submitted = st.form_submit_button("Generate health plan")

if submitted:
    if not name:
        st.warning("Please enter the child's name.")
    elif not eating_habits or not mood:
        st.warning("Please fill in eating habits and mood.")
    else:
        with st.spinner("Generating personalized health plan…"):
            try:
                profile = ChildHealthProfile(
                    name=name or None,
                    age=age,
                    gender=gender,
                    height_cm=height_cm,
                    weight_kg=weight_kg,
                    sleep_hours=sleep_hours,
                    screen_time_hours=screen_time_hours,
                    physical_activity_level=physical_activity_level,
                    eating_habits=eating_habits,
                    mood=mood,
                    symptoms=symptoms or None,
                )
                plan = generate_health_plan(profile)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        st.success("Here’s your child’s personalized health plan.")

        score = plan.get("Wellness Score") or plan.get("Wellness score")
        if score is not None:
            try:
                score_val = int(score) if isinstance(score, (int, float)) else int(str(score).replace("%", "").strip())
            except (ValueError, TypeError):
                score_val = None
            if score_val is not None:
                st.metric("Wellness Score", f"{score_val}/100")

        for key in plan:
            if key in ("Wellness Score", "Wellness score", "childProfile"):
                continue
            value = plan[key]
            with st.container():
                st.subheader(_format_key(key))
                md = _value_to_markdown(value)
                if md:
                    st.markdown(md)
                else:
                    st.write(value)
                st.divider()

        st.divider()
        st.caption("This is AI-generated guidance. Always consult a healthcare provider for medical decisions.")
