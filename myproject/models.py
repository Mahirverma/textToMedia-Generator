from . import db
from datetime import datetime
import json


class UserPrompt(db.Model):
    """
    Represents a user's prompt and the associated generated content.
    """
    __tablename__ = 'user_prompts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    prompt = db.Column(db.Text, nullable=False)
    video_paths = db.Column(db.Text, default="[]")  # Store as JSON list
    image_paths = db.Column(db.Text, default="[]")  # Store as JSON list
    # Status: Pending, Generating, Analyzing, Completed
    status = db.Column(db.String(20), default="Pending")
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_video_paths(self, paths):
        """Helper method to serialize video paths."""
        self.video_paths = json.dumps(paths)

    def get_video_paths(self):
        """Helper method to deserialize video paths."""
        return json.loads(self.video_paths)

    def set_image_paths(self, paths):
        """Helper method to serialize image paths."""
        self.image_paths = json.dumps(paths)

    def get_image_paths(self):
        """Helper method to deserialize image paths."""
        return json.loads(self.image_paths)

    def __repr__(self):
        return f"<UserPrompt {self.user_id}: {self.status}>"


class UserLog(db.Model):
    """
    Logs user actions, such as login attempts and content views.
    """
    __tablename__ = 'user_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    # e.g., "Login", "View Content"
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserLog {self.user_id}: {self.action} at {self.timestamp}>"


class ContentGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    image_paths = db.Column(db.PickleType)  # Store paths of generated images
    video_paths = db.Column(db.PickleType)  # Store paths of generated videos
    status = db.Column(db.String(50), default="Processing")
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, prompt, status, image_paths=None, video_paths=None):
        self.user_id = user_id
        self.prompt = prompt
        self.status = status
        self.image_paths = image_paths if image_paths else []
        self.video_paths = video_paths if video_paths else []

    def __repr__(self):
        return f"<ContentGeneration {self.user_id} - {self.status}>"
