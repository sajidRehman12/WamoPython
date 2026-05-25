from celery import Celery

app = Celery(
    "myapp",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@app.task
def add(x, y):
    return x + y

@app.task
def send_email(to, subject, body):
    print(f"Sending email to {to}: [{subject}] {body}")
    return f"Email sent to {to}"