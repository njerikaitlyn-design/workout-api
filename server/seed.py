#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # Clear the join table first, then the tables it points to
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    squats = Exercise(name='Squats', category='Strength', equipment_needed=False)
    bench = Exercise(name='Bench Press', category='Strength', equipment_needed=True)
    plank = Exercise(name='Plank', category='Core', equipment_needed=False)
    running = Exercise(name='Running', category='Cardio', equipment_needed=False)

    leg_day = Workout(date=date(2026, 10, 20), duration_minutes=60, notes='Focus on form')
    upper_body = Workout(date=date(2026, 10, 22), duration_minutes=45, notes='Heavy day')
    cardio_core = Workout(date=date(2026, 10, 24), duration_minutes=30)

    db.session.add_all([squats, bench, plank, running, leg_day, upper_body, cardio_core])
    db.session.commit()

    links = [
        WorkoutExercise(workout=leg_day, exercise=squats, reps=10, sets=4),
        WorkoutExercise(workout=leg_day, exercise=plank, duration_seconds=60),
        WorkoutExercise(workout=upper_body, exercise=bench, reps=8, sets=4),
        WorkoutExercise(workout=upper_body, exercise=plank, duration_seconds=45),
        WorkoutExercise(workout=cardio_core, exercise=running, duration_seconds=900),
        WorkoutExercise(workout=cardio_core, exercise=plank, duration_seconds=90),
    ]
    db.session.add_all(links)
    db.session.commit()

    print('Database seeded!')