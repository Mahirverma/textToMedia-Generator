from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_migrate import Migrate
from celery import Celery
from flask_login import LoginManager
import os

celery = None  # Placeholder for the Celery instance

# Create a login manager object
login_manager = LoginManager()


def initialize_celery(app):
    """Set up the Celery instance."""
    global celery
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery


"""Initialize the Flask app."""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text_to_media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Redis for task queue
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# For email notifications (adjust as needed)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'

db = SQLAlchemy(app)
mail = Mail(app)

# Initialize extensions
Migrate(app, db)
initialize_celery(app)

# Ensure media storage directory exists
os.makedirs('media/generated_content', exist_ok=True)

with app.app_context():
    from .models import UserPrompt
    db.create_all()


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',  # Use Redis for task queue
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
app.autodiscover_tasks(['myproject.tasks'])

# We can now pass in our app to the login manager
# login_manager.init_app(app)

# Tell users what view to go to when they need to login.
# login_manager.login_view = "login"
