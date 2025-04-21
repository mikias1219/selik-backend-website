import os

# Directory to store uploaded images
UPLOAD_DIR = os.path.join(os.getcwd(), 'app/static/images')

# Ensure the directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
