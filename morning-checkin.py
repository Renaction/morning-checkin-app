#!/usr/bin/env python3
"""
Morning Check-in App
A simple utility to log your daily plans and intentions
"""

import datetime
import json
import os

def load_checkins():
    """Load previous check-ins from file"""
    if os.path.exists("checkins.json"):
        try:
            with open("checkins.json", "r") as f:
                return [json.loads(line) for line in f]
        except Exception:
            return []
    return []

def save_checkin(checkin_data):
    """Save check-in data to file"""
    try:
        with open("checkins.json", "a") as f:
            f.write(json.dumps(checkin_data) + "\n")
        return True
    except Exception as e:
        print(f"Error saving check-in: {e}")
        return False

def display_previous_checkins():
    """Display recent check-ins"""
    checkins = load_checkins()
    if checkins:
        print("\n📅 Recent Check-ins:")
        print("-" * 40)
        for checkin in checkins[-3:]:  # Show last 3
            date = checkin.get("date", "Unknown")
            plans = checkin.get("plans", [])
            mood = checkin.get("mood", "N/A")
            print(f"Date: {date}")
            print(f"Mood: {mood}")
            print("Plans:")
            for i, plan in enumerate(plans, 1):
                print(f"  {i}. {plan}")
            print("-" * 40)

def get_user_input():
    """Get user input for today's check-in"""
    print("\n🌅 Good morning! Let's plan your day.")
    print("=" * 40)

    # Get mood/energy level
    print("\nHow are you feeling today?")
    mood_options = {
        "1": "😴 Sleepy/Low energy",
        "2": "😐 Neutral/Okay",
        "3": "😊 Good/Energetic",
        "4": "🚀 Excellent/Super motivated"
    }

    for key, value in mood_options.items():
        print(f"{key}. {value}")

    mood_choice = input("\nSelect your mood (1-4): ").strip()
    mood = mood_options.get(mood_choice, "Unknown")

    # Get daily plans
    print("\n📝 What do you plan to accomplish today?")
    print("Enter your plans one by one. Press Enter on an empty line to finish.")

    plans = []
    while True:
        plan = input(f"Plan #{len(plans) + 1}: ").strip()
        if not plan:
            break
        plans.append(plan)

    return mood, plans

def main():
    """Main function"""
    print("🌟 Morning Check-in App")
    print("=" * 30)

    # Show previous check-ins
    display_previous_checkins()

    # Get today's input
    mood, plans = get_user_input()

    if not plans:
        print("\nNo plans entered. Have a great day anyway! 🌈")
        return

    # Create check-in record
    checkin_data = {
        "date": datetime.date.today().isoformat(),
        "timestamp": datetime.datetime.now().isoformat(),
        "mood": mood,
        "plans": plans
    }

    # Save and confirm
    if save_checkin(checkin_data):
        print(f"\n✅ Check-in saved for {datetime.date.today().strftime('%B %d, %Y')}")
        print(f"\nYour plans for today:")
        for i, plan in enumerate(plans, 1):
            print(f"  {i}. {plan}")
        print(f"\nMood: {mood}")
        print("\nHave a productive day! 🎯")
    else:
        print("\n❌ Error saving check-in. Please try again.")

if __name__ == "__main__":
    main()