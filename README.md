# Morning Check-in App

A simple Python utility to help you plan and track your daily intentions.

## Features

- 🌅 Daily mood check-in
- 📝 Plan tracking
- 📅 History of previous check-ins
- 💾 Local JSON storage

## Usage

Run the app:
```bash
python morning-checkin.py
```

The app will:
1. Show your recent check-ins
2. Ask about your mood/energy level
3. Let you enter your plans for the day
4. Save everything to `checkins.json`

## Requirements

- Python 3.6+
- No additional dependencies required

## Data Storage

Check-ins are stored locally in `checkins.json` with the following format:
```json
{
  "date": "2024-12-02",
  "timestamp": "2024-12-02T08:30:00",
  "mood": "😊 Good/Energetic",
  "plans": ["Finish project", "Go for a walk", "Read for 30 minutes"]
}
```