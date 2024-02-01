from . import models
import string
import random
import os
import logging
import boto3
from botocore.exceptions import ClientError
from app import models
from PIL import Image
import io
from fastapi import HTTPException, status
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import cloudinary
import cloudinary.uploader
import cloudinary.api
from passlib.context import CryptContext

load_dotenv()

ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_IMAGES_BUCKET = os.getenv('AFRIBIDS_IMAGES_BUCKET')
cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY')
cloudinary_secret_key = os.getenv('CLOUDINARY_API_SECRET')
cloudinary_cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')

config = cloudinary.config(
        cloud_name = cloudinary_cloud_name,
        api_key = cloudinary_api_key,
        api_secret = cloudinary_secret_key,
        secure=True
    )
passwordd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



# generate unique username
def generate_unique_username(db, display_name):
    base_username = display_name.lower().replace(' ', '_')
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    potential_username = base_username + suffix
    existing_user = db.query(models.User).filter(models.User.username == potential_username).first()
    
    while existing_user:
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        potential_username = base_username + suffix
        existing_user = db.query(models.User).filter(models.User.username == potential_username).first()

    return potential_username


# image uploads to cloudinary

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================

def upload_to_cloudinary(images, auction_id):
    if not images:
        raise HTTPException(status_code=500, detail='Something went wrong') 
    
    upload_status = False
    image_urls = {}
    for image in images:
        image_name = image.filename.split('.')[:-1]
        public_id = f"{auction_id}{image_name}"
        cloudinary.uploader.upload(
            image.file, 
            public_id = public_id,
            unique_filename = True
        )

        image_url = cloudinary.CloudinaryImage(public_id).build_url(width=720)
        image_urls[image.filename] = image_url
        upload_status = True

    return upload_status, image_urls
      
def save_image_info(db, image_urls, auction_id):  
    try:
        for image,url in image_urls.items():
            image_item = models.AuctionImages(image_url=url, image_description=image, auction_id=auction_id)
            db.add(image_item)

        db.commit()

    except Exception as error:
        db.rollback()
        raise error

                    
def generate_random_image():
    image = Image.new("RGB", (300, 300)) 
    image_stream = io.BytesIO()
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)
    return image_stream


# security

### password hashing
def hash_passwords(raw_password:str):
    return passwordd_context.hash(raw_password)

### logins
def login():
    pass