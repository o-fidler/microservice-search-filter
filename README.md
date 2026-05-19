# Search/Filter Microservice

## Description

This microservice accepts a dataset of items and one or more filter parameters, then returns only the items that match the given criteria. It supports:

- **Keyword search** — case-insensitive match against an item's `name` and `description` fields
- **Category filter** — exact (case-insensitive) match against an item's `category` field
- **Combined filtering** — both keyword and category applied simultaneously (AND logic)

The microservice runs locally on **port 5003** and communicates via **REST API** using JSON over HTTP.

---

## How to Run

```bash
pip install flask
python microservice.py
```

The service will start at `http://localhost:5003`.

---

## Communication Contract

### Requesting Data

Send a **POST** request to `/search` with a JSON body containing:

| Field | Type | Required | Description |
|---|---|---|---|
| `data` | array | ✅ Yes | List of item objects to filter. Each item should have `name`, `category`, and optionally `description`. |
| `keyword` | string | ⚠️ At least one | Case-insensitive substring matched against `name` and `description`. |
| `category` | string | ⚠️ At least one | Exact (case-insensitive) match against item's `category` field. |

At least one of `keyword` or `category` must be included.

#### Example Request

```python
import requests

payload = {
    "data": [
        {"name": "Push-up",  "category": "strength", "description": "Upper body bodyweight exercise"},
        {"name": "Squat",    "category": "strength", "description": "Lower body compound movement"},
        {"name": "Running",  "category": "cardio",   "description": "Sustained aerobic exercise"}
    ],
    "keyword": "upper",
    "category": "strength"
}

response = requests.post("http://localhost:5003/search", json=payload)
```

---

### Receiving Data

The microservice returns a **JSON object** with a `results` key. The value is an array of items from the input dataset that matched all provided filter criteria.

- If no items match, `results` will be an **empty array** (not an error).
- Each item in `results` has the same structure as items in the original input.

#### Response Structure

```json
{
  "results": [
    {
      "name": "Push-up",
      "category": "strength",
      "description": "Upper body bodyweight exercise"
    }
  ]
}
```

#### Example: Receiving and Using the Response

```python
response = requests.post("http://localhost:5003/search", json=payload)
results = response.json()["results"]

for item in results:
    print(item["name"])
```

#### Error Responses

| Status | Cause |
|---|---|
| `400` | Missing or invalid `data` field, or neither `keyword` nor `category` provided |

```json
{ "error": "At least one of 'keyword' or 'category' must be provided." }
```

---

## UML Sequence Diagram

```
  Calling Program                 Search/Filter Microservice
       |                                      |
       |  POST /search                        |
       |  Body: { data: [...],                |
       |           keyword: "upper",          |
       |           category: "strength" }     |
       |------------------------------------->|
       |                                      |
       |                                      |  Validate request body
       |                                      |  (check data, keyword, category)
       |                                      |
       |                                      |  Apply keyword filter
       |                                      |  (case-insensitive match on
       |                                      |   name + description)
       |                                      |
       |                                      |  Apply category filter
       |                                      |  (exact case-insensitive match
       |                                      |   on category field)
       |                                      |
       |  HTTP 200 OK                         |
       |  Body: { "results": [ ... ] }        |
       |<-------------------------------------|
       |                                      |
       |  Read response.json()["results"]     |
       |  Iterate over matching items         |
       |                                      |

       --- Error path (missing data or no filters) ---

  Calling Program                 Search/Filter Microservice
       |                                      |
       |  POST /search                        |
       |  Body: { keyword: "upper" }          |
       |  (missing "data" field)              |
       |------------------------------------->|
       |                                      |
       |                                      |  Validation fails:
       |                                      |  "data" field not found
       |                                      |
       |  HTTP 400 Bad Request                |
       |  Body: { "error": "..." }            |
       |<-------------------------------------|
       |                                      |
       |  Handle error in calling program     |
       |                                      |
```

---

## Running the Test Program

With the microservice running in one terminal, open a second terminal and run:

```bash
python test_microservice.py
```

The test program demonstrates:
1. Keyword-only filtering
2. Category-only filtering
3. Combined keyword + category filtering
4. A keyword that matches nothing (returns empty array)
5. Case-insensitive keyword matching
6. Error: missing `data` field
7. Error: no filters provided
