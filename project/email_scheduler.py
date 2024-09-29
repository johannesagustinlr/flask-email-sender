from model import db, EmailSchedule
from celery import Celery
from app import app

celery = Celery(
    app.name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
)
celery.conf.update(app.config)


@celery.task
def email_scheduler(email_id):
    email = EmailSchedule.query.get(email_id)
    if email:
        print(f"Sending email: {email.email_subject} to recipients")
        email.is_sent = True
        db.session.commit()
        return f"Email {email_id} sent"
    return f"Email {email_id} not found"
