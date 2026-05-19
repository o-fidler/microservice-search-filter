import requests

BASE_URL = "http://localhost:5003/search"

SAMPLE_DATA = [
    {"name": "Push-up",  "category": "strength", "description": "Upper body bodyweight exercise"},
    {"name": "Squat",    "category": "strength", "description": "Lower body compound movement"},
    {"name": "Running",  "category": "cardio",   "description": "Sustained aerobic exercise"},
    {"name": "Plank",    "category": "core",     "description": "Upper body and core stability hold"},
    {"name": "Cycling",  "category": "cardio",   "description": "Low-impact aerobic exercise on a bike"},
    {"name": "Deadlift", "category": "strength", "description": "Full body posterior chain exercise"},
]

# keyword only
r = requests.post(BASE_URL, json={"data": SAMPLE_DATA, "keyword": "upper"})
print("keyword 'upper':", r.json())

# category only
r = requests.post(BASE_URL, json={"data": SAMPLE_DATA, "category": "strength"})
print("category 'strength':", r.json())

# keyword + category
r = requests.post(BASE_URL, json={"data": SAMPLE_DATA, "keyword": "upper", "category": "strength"})
print("keyword + category:", r.json())

# no matches
r = requests.post(BASE_URL, json={"data": SAMPLE_DATA, "keyword": "yoga"})
print("no matches:", r.json())

# case-insensitive
r = requests.post(BASE_URL, json={"data": SAMPLE_DATA, "keyword": "AEROBIC"})
print("case-insensitive 'AEROBIC':", r.json())

# error: missing data
r = requests.post(BASE_URL, json={"keyword": "upper"})
print("missing data field:", r.status_code, r.json())

# error: no filters
r = requests.post(BASE_URL, json={"data": SAMPLE_DATA})
print("no filters:", r.status_code, r.json())
