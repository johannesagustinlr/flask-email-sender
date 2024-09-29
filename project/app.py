from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
import os
from project.model import db, EmailSchedule
from datetime import datetime
from project.celery_worker import make_celery
import pytz

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///email_scheduler.db"
db.init_app(app)
app.config["CELERY_BROKER_URL"] = "sqla+sqlite:///celerydb.sqlite"
app.config["CELERY_RESULT_BACKEND"] = "db+sqlite:///results.sqlite"
app.config["TIMEZONE"] = "Asia/Singapore"


with app.app_context():
    db.create_all()

celery = make_celery(app)


@app.route("/")
def index():
    print(request.content_type)
    return render_template("form.html")


@app.post("/save_emails")
def save_emails():
    sg_tz = pytz.timezone("Asia/Singapore")
    if request.is_json:
        data = request.get_json()

        try:
            # Parse the incoming data
            event_id = data.get("event_id")
            email_subject = data.get("email_subject")
            email_content = data.get("email_content")
            timestamp_str = data.get(
                "timestamp",
            )  # Expected format: "2024-09-25T00:21"

            schedule_datetime = datetime.strptime(
                timestamp_str,
                "%Y-%m-%dT%H:%M",
            )
            schedule_sg_time = sg_tz.localize(schedule_datetime)
            email_schedule = EmailSchedule(
                event_id=event_id,
                email_subject=email_subject,
                email_content=email_content,
                timestamp=schedule_sg_time,
            )
            db.session.add(email_schedule)
            db.session.commit()
            utc_datetime = schedule_sg_time.astimezone(pytz.UTC)
            email_scheduler.apply_async(
                (email_schedule.id,),
                eta=utc_datetime,
            )
            return (
                jsonify(
                    {
                        "message": "Email scheduler saved successfully!",
                    }
                ),
                201,
            )
        except Exception as e:
            return (jsonify({"error": str(e)}), 400)
    elif (
        request.content_type == "application/x-www-form-urlencoded"
        or request.content_type == "multipart/form-data"
    ):
        try:

            event_id = int(request.form["event_id"])
            email_subject = request.form["email_subject"]
            email_content = request.form["email_content"]
            timestamp_str = request.form["timestamp"]
            schedule_datetime = datetime.strptime(
                timestamp_str,
                "%Y-%m-%dT%H:%M",
            )
            schedule_sg_time = sg_tz.localize(schedule_datetime)

            email_schedule = EmailSchedule(
                event_id=event_id,
                email_subject=email_subject,
                email_content=email_content,
                timestamp=schedule_sg_time,
            )
            db.session.add(email_schedule)
            db.session.commit()
            utc_datetime = schedule_sg_time.astimezone(pytz.UTC)

            email_scheduler.apply_async(
                (email_schedule.id,),
                eta=utc_datetime,
            )
            return redirect(url_for("save_emails_list"))
        except Exception as e:
            print(e)
            flash(
                "Error when saving data",
                "error",
            )
            return redirect(url_for("index"))

    else:
        return (jsonify({"error": "Unsupported Content-Type"}), 400)


@celery.task
def email_scheduler(email_id):
    email = EmailSchedule.query.get(email_id)
    if email:
        print(
            f"Sending email: {email.email_subject} to recipients",
        )
        email.is_sent = True
        db.session.commit()
        return f"Email {email_id} sent"
    return f"Email {email_id} not found"


@app.route("/email_save_list")
def save_emails_list():
    email_schedule = EmailSchedule.query.all()
    return render_template("email_list.html", email_schedule=email_schedule)


if __name__ == "__main__":
    app.run(debug=True)
