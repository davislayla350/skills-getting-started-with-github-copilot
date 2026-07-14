"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team for practices and matches",
        "schedule": "Daily practice, 4:00 PM - 6:00 PM; Matches on Saturdays",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Play pick-up games and develop basketball skills",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu"]
    },
    "Volleyball Team": {
        "description": "Competitive volleyball practices and seasonal matches",
        "schedule": "Mondays and Wednesdays, 4:30 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu"]
    },
    "Track and Field": {
        "description": "Sprint, distance, jumps, and throws training with meets",
        "schedule": "Daily practice, 3:30 PM - 5:00 PM; Meets on weekends",
        "max_participants": 40,
        "participants": ["ethan@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Swim training, stroke work, and swim meets",
        "schedule": "Mondays, Wednesdays, Fridays, 5:00 PM - 6:30 PM",
        "max_participants": 30,
        "participants": ["zoe@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis techniques and play friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ryan@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, stagecraft, and producing school plays",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 30,
        "participants": ["sophia@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques, editing, and portfolio building",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Club": {
        "description": "Instrument practice, ensemble sessions, and performances",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["oliver@mergington.edu"]
    },
    "Ceramics Club": {
        "description": "Hand-building and wheel-throwing ceramics projects",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": ["nora@mergington.edu"]
    },
    "Choir": {
        "description": "Vocal ensemble rehearsals and choral performances",
        "schedule": "Tuesdays, 4:30 PM - 6:00 PM",
        "max_participants": 30,
        "participants": ["lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, science fairs, and research projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive and practice debates on current topics",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["daniel@mergington.edu"]
    },
    "Math Club": {
        "description": "Problem solving, competitions, and math enrichment",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["grace@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for competitions and projects",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["jack@mergington.edu"]
    },
    "History Club": {
        "description": "Discuss historical events, research projects, and competitions",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["hannah@mergington.edu"]
    },
    "Philosophy Club": {
        "description": "Critical thinking, readings, and philosophical discussions",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["owen@mergington.edu"]
    }
}



@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if the student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
   
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

# New endpoint to remove a participant
@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in activity")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
