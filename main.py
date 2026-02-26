from data_models import ChildHealthProfile
from health_engine import generate_health_plan

def main():
    sample_child = ChildHealthProfile(
        name="Aarav",
        age=10,
        gender="Male",
        height_cm=138,
        weight_kg=42,
        sleep_hours=7,
        screen_time_hours=4,
        physical_activity_level="Low",
        eating_habits="Prefers junk food, low vegetables",
        mood="Often tired",
        symptoms="Occasional headaches"
    )

    health_plan = generate_health_plan(sample_child)

    print("\n🩺 AI Health Companion Report\n")
    for key, value in health_plan.items():
        print(f"{key}:\n{value}\n")

if __name__ == "__main__":
    main()