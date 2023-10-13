from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "asd!ljd5dlLkjK"
app.permanent_session_lifetime = timedelta(days=60)

app.json.ensure_ascii = False
app.json.compact = False

from app import views
