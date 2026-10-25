# Workout Tracker API

A backend REST API for personal trainers to track workouts and the exercises inside them. Built with **Flask**, **SQLAlchemy**, **Flask-Migrate** and **Marshmallow**.


## Description

Trainers can create workouts, create exercises, and add exercises to workouts with reps, sets, or a duration. Exercises are **reusable**: the same exercise (for example, Squats) can appear in many workouts. Each pairing stores its own reps, sets, and duration.

## Features

- Create, view, and delete workouts
- Create, view, and delete exercises
- Add an exercise to a workout with reps, sets, or duration
- View a workout with all its exercises and their reps/sets/duration
- View an exercise with all the workouts it appears in
- Deleting a workout or exercise also deletes its linked workout exercises
- Validation at three levels: database, model, and schema

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Language |
| Flask 2.2.2 | Web framework |
| Flask-SQLAlchemy 3.0.3 | Database models (ORM) |
| Flask-Migrate 3.1.0 | Database migrations |
| Marshmallow 3.20.1 | Serialization and request validation |
| SQLite | Database |
| Pipenv | Dependency management |

## Project Structure

```
workout-api/
├── Pipfile
├── Pipfile.lock
├── README.md
└── server/
    ├── app.py          # Flask app and all endpoints
    ├── models.py       # Database models, relationships, constraints, validations
    ├── schemas.py      # Marshmallow schemas and schema validations
    ├── seed.py         # Resets the database and adds example data
    └── migrations/     # Database migration files (created by flask db init)
```

## Data Model

Three tables:

**Exercise**: a reusable exercise

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| name | String | Required, unique |
| category | String | Required |
| equipment_needed | Boolean | Defaults to false |

**Workout**: a single workout session

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| date | Date | Required |
| duration_minutes | Integer | Required, must be greater than 0 |
| notes | Text | Optional |

**WorkoutExercise**: join table linking workouts and exercises

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| workout_id | Integer | Foreign key to workouts, required |
| exercise_id | Integer | Foreign key to exercises, required |
| reps | Integer | Optional, must be greater than 0 |
| sets | Integer | Optional, must be greater than 0 |
| duration_seconds | Integer | Optional, must be greater than 0 |

### Relationships

- A Workout has many WorkoutExercises
- An Exercise has many WorkoutExercises
- A WorkoutExercise belongs to one Workout and one Exercise
- A Workout has many Exercises through WorkoutExercises
- An Exercise has many Workouts through WorkoutExercises

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/njerikaitlyn-design/workout-api.git
cd workout-api
```

**2. Install dependencies and activate the virtual environment**

```bash
pipenv install
pipenv shell
```

**3. Set up the database** (run these from inside the `server/` folder)

```bash
cd server
export FLASK_APP=app.py
flask db init
flask db migrate -m "Create exercises, workouts and workout_exercises tables"
flask db upgrade head
```

**4. Seed the database with example data**

```bash
python seed.py
```

> Running `seed.py` again clears all existing data and re-creates the examples, so it never creates duplicates.

### Seed data

- **4 exercises:** Squats, Bench Press, Plank, Running
- **3 workouts:** Leg Day, Upper Body, Cardio and Core
- **6 workout exercises** linking them together

## Running the App

From inside the `server/` folder:

```bash
flask run --port 5555
```

The API is now available at **http://localhost:5555**

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its exercises, including reps, sets, and duration |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout and its workout exercises |

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise with the workouts it appears in |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its workout exercises |

### Adding an exercise to a workout

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps/sets or a duration |

### Request bodies

**POST /workouts**

| Field | Type | Required |
|-------|------|----------|
| date | string (`YYYY-MM-DD`) | Yes |
| duration_minutes | integer | Yes |
| notes | string | No |

**POST /exercises**

| Field | Type | Required |
|-------|------|----------|
| name | string | Yes |
| category | string | Yes |
| equipment_needed | boolean | No (defaults to false) |

**POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises**

| Field | Type | Required |
|-------|------|----------|
| reps | integer | Provide reps **and** sets, or a duration |
| sets | integer | Provide reps **and** sets, or a duration |
| duration_seconds | integer | Provide reps **and** sets, or a duration |

## Example Requests and Responses

**Create an exercise**

```bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Lunges", "category": "Strength", "equipment_needed": false}'
```

Response `201 Created`:

```json
{
  "id": 5,
  "name": "Lunges",
  "category": "Strength",
  "equipment_needed": false
}
```

**Create a workout**

```bash
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-10-25", "duration_minutes": 50, "notes": "Leg focus"}'
```

**Add an exercise to a workout** (workout 3, exercise 2)

```bash
curl -X POST http://localhost:5555/workouts/3/exercises/2/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 10, "sets": 3}'
```

Response `201 Created`:

```json
{
  "id": 7,
  "workout_id": 3,
  "exercise_id": 2,
  "reps": 10,
  "sets": 3,
  "duration_seconds": null,
  "exercise": {"id": 2, "name": "Bench Press", "category": "Strength", "equipment_needed": true},
  "workout": {"id": 3, "date": "2026-10-24", "duration_minutes": 30, "notes": null}
}
```

**View a workout with its exercises**

```bash
curl http://localhost:5555/workouts/1
```

Response `200 OK`:

```json
{
  "id": 1,
  "date": "2026-10-20",
  "duration_minutes": 60,
  "notes": "Focus on form",
  "workout_exercises": [
    {
      "id": 1,
      "reps": 10,
      "sets": 4,
      "duration_seconds": null,
      "exercise": {"id": 1, "name": "Squats", "category": "Strength", "equipment_needed": false}
    },
    {
      "id": 2,
      "reps": null,
      "sets": null,
      "duration_seconds": 60,
      "exercise": {"id": 3, "name": "Plank", "category": "Core", "equipment_needed": false}
    }
  ]
}
```

**View an exercise with its workouts**

```bash
curl http://localhost:5555/exercises/1
```

**Delete a workout**

```bash
curl -X DELETE http://localhost:5555/workouts/1
```

Response: `204 No Content` (empty body)

## Validations

The app checks data at three levels, so bad data is stopped as early as possible.

### Table constraints (enforced by the database)

- Exercise `name` must be unique
- Exercise `name`, `category` and Workout `date`, `duration_minutes` cannot be empty
- Workout `duration_minutes` must be greater than 0
- WorkoutExercise `reps` and `sets` must be greater than 0

### Model validations (enforced by SQLAlchemy models)

- Exercise `name` and `category` cannot be blank or only spaces (extra spaces are trimmed)
- Workout `duration_minutes` must be greater than 0
- WorkoutExercise `reps`, `sets`, and `duration_seconds` must be greater than 0

### Schema validations (enforced by Marshmallow)

- Exercise `name` must be 1 to 100 characters and cannot be blank
- Exercise `category` must be 1 to 50 characters
- Workout `duration_minutes` must be at least 1
- Workout `notes` can be at most 500 characters
- WorkoutExercise `reps`, `sets` and `duration_seconds` must be at least 1
- Each WorkoutExercise needs **both reps and sets, or a duration_seconds**

## Error Responses

| Status | Meaning | When it happens |
|--------|---------|-----------------|
| 400 Bad Request | Invalid data | Failed a validation or constraint (for example, a duplicate exercise name) |
| 404 Not Found | Resource missing | The workout or exercise id does not exist |

Schema validation errors list the problem for each field:

```json
{
  "errors": {
    "duration_minutes": ["Must be greater than or equal to 1."]
  }
}
```

Model and database errors return a single message:

```json
{
  "error": "Exercise name cannot be empty"
}
```

Missing resources return:

```json
{
  "error": "Workout not found"
}
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `flask: command not found` | Run `pipenv shell` first to activate the environment |
| `Error: Could not locate a Flask application` | Run `export FLASK_APP=app.py` from inside the `server/` folder |
| Migration commands fail | Make sure you are inside the `server/` folder |
| `table already exists` error | Delete `server/instance/app.db` and the `server/migrations/` folder, then repeat the database setup steps |
| Port 5555 already in use | Stop the other process, or run `flask run --port 5556` |