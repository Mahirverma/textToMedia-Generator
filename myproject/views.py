from flask import Flask, render_template, request, redirect, url_for, flash
from myproject import app,db
from .models import UserPrompt, UserLog
from .tasks import generate_image_task, generate_video_task
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the home page where users can submit prompts.
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        prompt = request.form['prompt']

        # Check if a record already exists for the user
        existing_prompt = UserPrompt.query.filter_by(user_id=user_id).first()
        if existing_prompt:
            flash("A prompt for this user is already being processed or completed.")
            return redirect(url_for('gallery', user_id=user_id))

        # Add new prompt to the database
        new_prompt = UserPrompt(
            user_id=user_id, prompt=prompt, status="Pending")
        db.session.add(new_prompt)
        db.session.commit()

        # Log the action
        log_user_action(user_id, "Submitted Prompt")

        # Trigger content generation task
        generate_content.delay(user_id, prompt)

        flash("Your content generation has started! Please check back later.")
        return redirect(url_for('gallery', user_id=user_id))

    return render_template('index.html')


@app.route('/gallery/<user_id>')
def gallery(user_id):
    """
    Displays the generated content or status of the user's request.
    """
    user_prompt = UserPrompt.query.filter_by(user_id=user_id).first()

    if not user_prompt:
        flash("No content found for the provided user ID.")
        return redirect(url_for('index'))

    # Log the action
    log_user_action(user_id, "Viewed Gallery")

    if user_prompt.status in ["Generating", "Analyzing"]:
        return render_template('status.html', status=user_prompt.status)

    # Deserialize video and image paths
    videos = user_prompt.get_video_paths()
    images = user_prompt.get_image_paths()

    return render_template('gallery.html', videos=videos, images=images, user_id=user_id)


@app.route('/generate_content', methods=['POST'])
def generate_content():
    user_id = request.form['user_id']
    prompt = request.form['prompt']
    content_type = request.form['content_type']

    # Add a new content generation task
    if content_type == 'image':
        generate_image_task.apply_async(args=[user_id, prompt])
    elif content_type == 'video':
        generate_video_task.apply_async(args=[user_id, prompt])

    # Redirect to a status page while the task is being processed
    return redirect(url_for('status', user_id=user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return redirect(url_for('status', user_id=user_id))

    return render_template('login.html')


def log_user_action(user_id, action):
    """
    Logs user actions for tracking and analytics.
    """
    new_log = UserLog(user_id=user_id, action=action,
                      timestamp=datetime.utcnow())
    db.session.add(new_log)
    db.session.commit()
