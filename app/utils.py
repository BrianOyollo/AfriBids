from . import models
import string
import random
import os
from app import models
from PIL import Image
import io
from fastapi import HTTPException, status



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

async def upload_auction_images(db, images,auction_id):
    upload_to = "app/images/"
    
    try:
        for image in images:
            file_name = f"{auction_id}_{image.filename}"
            file_path = os.path.join(upload_to,file_name)
            file_content = await image.read()

            # replace with uploading to s3
            with open(file_path, 'wb') as file:
                file.write(file_content)


            # save image info into AuctionImages
            image_item = models.AuctionImages(image_url=file_name, auction_id=auction_id)
            db.add(image_item)
        db.commit()
            # db.refresh(image_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must provide at least one image for the auction')
                    
def generate_random_image():
    image = Image.new("RGB", (300, 300)) 
    image_stream = io.BytesIO()
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)
    return image_stream