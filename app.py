from flask import Flask, render_template, jsonify, session, send_from_directory
import random
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Square dimensions
square_size = 100
margin = 10

# Image names for the memory game
image_names = [
    "aluminum.png", "beryllium.png", "boron.png", "carbon.png",
    "fluorine.png", "helium.png", "hydrogen.png", "lithium.png",
    "magnesium.png", "neon.png", "nitrogen.png", "oxygen.png"
]

# Directory for the original images
original_images_dir = 'static/images/'

# Directory to save resized images
resized_images_dir = 'static/images_resized/'

# Ensure the resized images directory exists
os.makedirs(resized_images_dir, exist_ok=True)

# Function to resize images
def resize_images():
    for image_name in image_names:
        image_path = os.path.join(original_images_dir, image_name)
        resized_image_path = os.path.join(resized_images_dir, image_name)

        # Open the image
        with Image.open(image_path) as img:
            # Resize the image to 100x100
            img = img.resize((square_size, square_size))
            # Save the resized image
            img.save(resized_image_path)

# Call the function to resize images when the server starts
resize_images()

# Function to shuffle and start a new game
def start_game():
    all_images = list(image_names) * 2  # Pairing images
    random.shuffle(all_images)

    cards = [{"value": value, "flipped": False, "matched": False} for value in all_images]
    
    session['cards'] = cards

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game')
def start_new_game():
    start_game()  # Start a new game
    return jsonify({'cards': session['cards']})

@app.route('/get_game_state')
def get_game_state():
    return jsonify({
        'cards': session.get('cards')
    })

# Route to serve resized images
@app.route('/static/images_resized/<filename>')
def serve_resized_image(filename):
    return send_from_directory(resized_images_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
