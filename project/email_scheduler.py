from project.model import db, EmailSchedule


@celery.task
def schedule_email(email_id):
    email = Email.query.get(email_id)
    if email:
        # Simulate sending the email (you can integrate a real email service here)
        print(f"Sending email: {email.email_subject} to recipients")
        email.is_sent = True
        db.session.commit()
        return f"Email {email_id} sent"
    return f"Email {email_id} not found"
