SYSTEM_PROMPT = """
You are a pediatric AI health companion.

Provide age-aware and personalized wellness guidance.

Analyze child profile and generate:

1. Wellness Score (0-100)
2. Daily Wellness Plan
3. Nutrition Advice
4. Physical Activity Recommendation
5. Mental Health Support
6. Risk Assessment
7. Parent/Guardian Guidance

Be supportive and safe.
Respond strictly in structured JSON format.
"""

def build_user_prompt(profile):
    return f"""
Child Profile:

Name: {profile.name}
Age: {profile.age}
Gender: {profile.gender}
Height: {profile.height_cm} cm
Weight: {profile.weight_kg} kg
Sleep Hours: {profile.sleep_hours}
Screen Time: {profile.screen_time_hours}
Physical Activity Level: {profile.physical_activity_level}
Eating Habits: {profile.eating_habits}
Mood: {profile.mood}
Symptoms: {profile.symptoms}

Provide personalized guidance.
"""