
from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError

from app import db
from app.models.note import Note
from app.schemas.note_schema import note_schema, notes_schema
from app.auth.decorators import login_required

notes_bp = Blueprint("notes", __name__, url_prefix="/api")


# GET: View all notes belonging to the logged-in user
@notes_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
    notes = Note.query.filter_by(
        user_id=g.current_user.id
    ).all()

    return jsonify({
        "notes": notes_schema.dump(notes)
    }), 200


# GET: View one note
@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
@login_required
def get_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=g.current_user.id
    ).first()

    if note is None:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({
        "note": note_schema.dump(note)
    }), 200


# POST: Create a new note
@notes_bp.route("/notes", methods=["POST"])
@login_required
def create_note():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        validated_data = note_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    new_note = Note(
        title=validated_data["title"],
        content=validated_data.get("content", ""),
        user_id=g.current_user.id
    )

    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        "message": "Note created successfully",
        "note": note_schema.dump(new_note)
    }), 201


# PUT: Update an existing note
@notes_bp.route("/notes/<int:note_id>", methods=["PUT"])
@login_required
def update_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=g.current_user.id
    ).first()

    if note is None:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        validated_data = note_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "title" in validated_data:
        note.title = validated_data["title"]

    if "content" in validated_data:
        note.content = validated_data["content"]

    db.session.commit()

    return jsonify({
        "message": "Note updated successfully",
        "note": note_schema.dump(note)
    }), 200


# DELETE: Delete a note
@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=g.current_user.id
    ).first()

    if note is None:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted successfully"
    }), 200


