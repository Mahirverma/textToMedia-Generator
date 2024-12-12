import openai
from runwayml import RunwayML
import requests
from . import celery
from time import sleep
from os.path import join
from myproject.models import ContentGeneration

runway = RunwayML()


@celery.task
def generate_image_task(user_id, prompt):
    try:
        # Generate an image using OpenAI's DALL·E
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Size of the generated image
        )
        # Get the URL of the generated image
        image_url = response['data'][0]['url']

        # Save image to disk
        image_path = save_image_from_url(image_url, user_id)

        # Save the content generation record in the database
        content = ContentGeneration(
            user_id=user_id, prompt=prompt, status="Completed", image_paths=[image_path])
        content.save()

        return {"status": "Completed", "user_id": user_id, "image_path": image_path}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}


def save_image_from_url(url, user_id):
    # Define the folder path
    folder_path = f"generated_content/{user_id}/images/"
    file_name = url.split("/")[-1]  # Get the image filename from the URL

    # Download the image and save it
    img_data = requests.get(url).content
    image_path = join(folder_path, file_name)

    with open(image_path, 'wb') as f:
        f.write(img_data)

    return image_path


@celery.task
def generate_video_task(user_id, prompt):
    try:
        # Generate a video using RunwayML
        response = runway.run(
            model="text2video",
            inputs={"prompt": prompt}
        )

        # Get the video path or URL from the response
        # Assuming the response contains a URL to the video
        video_url = response['video_url']
        video_path = save_video_from_url(video_url, user_id)

        # Save the content generation record in the database
        content = ContentGeneration(
            user_id=user_id, prompt=prompt, status="Completed", video_paths=[video_path])
        content.save()

        return {"status": "Completed", "user_id": user_id, "video_path": video_path}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}


def save_video_from_url(url, user_id):
    # Define the folder path
    folder_path = f"generated_content/{user_id}/videos/"
    file_name = url.split("/")[-1]  # Get the video filename from the URL

    # Download the video and save it
    video_data = requests.get(url).content
    video_path = join(folder_path, file_name)

    with open(video_path, 'wb') as f:
        f.write(video_data)

    return video_path
