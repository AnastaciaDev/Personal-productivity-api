from marshmallow import Schema, fields, validate


class UserSchema(Schema):

    id = fields.Integer(dump_only=True)

    username = fields.String(
        required=True,
        validate=validate.Length(min=3)
    )

    email = fields.Email(
        required=True,
        validate=validate.Length(max=120)
    )

    password = fields.String(
        load_only=True,
        required=True,
        validate=validate.Length(min=8)
    )

    created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()

