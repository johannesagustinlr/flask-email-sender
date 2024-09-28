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


app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///email_scheduler.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route(
    "/",
)
def index():
    print(request.content_type)
    return render_template("form.html")


@app.post(
    "/save_emails",
)
def save_emails():
    if request.is_json:
        print("json")
    elif (
        request.content_type == "application/x-www-form-urlencoded"
        or request.content_type == "multipart/form-data"
    ):
        try:
            print(request.form)
            event_id = int(request.form["event_id"])
            email_subject = request.form["email_subject"]

            email_schedule = EmailSchedule(
                event_id=event_id,
                email_subject=email_subject,
            )
            db.session.add(email_schedule)
            db.session.commit()
            return redirect(url_for("save_emails_list"))
        except Exception as e:
            print(e)
            flash("Error when saving data", "error")
            return redirect(url_for("index"))

    else:
        return jsonify({"error": "Unsupported Content-Type"}), 400


@app.route("/email_save_list")
def save_emails_list():
    email_schedule = EmailSchedule.query.all()
    return render_template("datalist.html", email_schedule=email_schedule)


if __name__ == "__main__":
    app.run(debug=True)
