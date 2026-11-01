
from datetime import datetime
from backports.zoneinfo import ZoneInfo
from app import db


kenya_timezone = ZoneInfo("Africa/Nairobi")

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    content = db.Column(db.Text, nullable=False, default="")

    created_at = db.Column(
    db.DateTime(timezone=True),
    default=lambda: datetime.now(kenya_timezone),
    nullable=False
    )

    updated_at = db.Column(
    db.DateTime(timezone=True),
    default=lambda: datetime.now(kenya_timezone),
    onupdate=lambda: datetime.now(kenya_timezone),
    nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.title}>"


