

# flask-email-sender

1. git clone this repo
2. cd to this repo directory
3. run python3 -m venv .venv
4. source .venv/bin/activate (linux)
5. pip install -r requirements.txt
6. flask run (for test) / gunicorn -w 4 -b 0.0.0.0:8000 project.app:app (for deployment)
7. celery -A project.app.celery worker --loglevel=info (for email scheduler and queue)
8. you can access via browser to input form localhost:5000 (flask run) / localhost:8000 (gunicorn)


Note : 
1. No validation for email, currently able to save to database but might failed when send the email if email is not valid , can send more than 1, seperate it using comma
2. currently event id and event subject is unique
3. currently cant let event id, event subject, event content, event recipents, timestamp empty
