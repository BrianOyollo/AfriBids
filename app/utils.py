from . import models
import string
import random

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