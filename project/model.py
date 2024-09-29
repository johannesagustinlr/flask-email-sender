from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EmailSchedule(db.Model):
    __tablename__ = "email_schedule"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, unique=True)
    email_subject = db.Column(db.String(120), unique=True, nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    is_sent = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        event_id,
        email_subject,
        email_content,
        timestamp,
    ):
        self.event_id = event_id
        self.email_subject = email_subject
        self.email_content = email_content
        self.timestamp = timestamp

    def __repr__(self):
        return f"{self.event_id}!"
