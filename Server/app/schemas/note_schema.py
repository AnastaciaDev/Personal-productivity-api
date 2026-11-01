from marshmallow import Schema, fields, validate


class NoteSchema(Schema):

    id = fields.Integer(dump_only=True)

    title = fields.String(
        required=True,
        validate=validate.Length(min=1, max=150)
    )

    content = fields.String(
        load_default=""
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


# Used when creating, viewing or updating one note
note_schema = NoteSchema()

# Used when displaying multiple notes
notes_schema = NoteSchema(many=True)

