from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)

    @validates('name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError('Name cannot be blank.')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    exercise = fields.Nested(ExerciseSchema, dump_only=True)
    workout = fields.Nested(WorkoutSchema, dump_only=True)

    @validates_schema
    def validate_effort(self, data, **kwargs):
        """Each entry needs reps/sets, or a duration."""
        has_reps_sets = data.get('reps') is not None and data.get('sets') is not None
        has_duration = data.get('duration_seconds') is not None
        if not (has_reps_sets or has_duration):
            raise ValidationError(
                'Provide both reps and sets, or a duration_seconds.'
            )


class WorkoutDetailSchema(WorkoutSchema):
    """A workout plus its exercises, with reps/sets/duration."""
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True,
        only=('id', 'reps', 'sets', 'duration_seconds', 'exercise'),
    )


class ExerciseDetailSchema(ExerciseSchema):
    """An exercise plus the workouts it appears in."""
    workouts = fields.Nested(WorkoutSchema, many=True, dump_only=True)