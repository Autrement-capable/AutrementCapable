from flask import Flask, send_file, render_template_string, request
import python_avatars as pa
import tempfile
from dictionaries import *
import os

app = Flask(__name__)

# Define other dictionaries for eyebrows, eyes, etc.

def create_avatar(style, background_color, top, eyebrows, eyes, nose, mouth, facial_hair, skin, hair_color, accessory, clothing, clothing_color):
    return pa.Avatar(
        style=style,
        background_color=background_color,
        top=top,
        eyebrows=eyebrows,
        eyes=eyes,
        nose=nose,
        mouth=mouth,
        facial_hair=facial_hair,
        skin=skin,
        hair_color=hair_color,
        accessory=accessory,
        clothing=clothing,
        clothing_color=clothing_color
    )

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Custom Avatar Generator</title>
    </head>
    <body>
        <h1>Custom Avatar Generator</h1>
        <div id="avatar">
            <img src="/avatar" alt="Avatar" id="avatar-image">
        </div>
        <div>
            <label for="style">Style:</label>
            <button onclick="changeOption('style', -1)">←</button>
            <span id="style-text">circle</span>
            <button onclick="changeOption('style', 1)">→</button>
        </div>
        <div>
            <label for="top">Top:</label>
            <button onclick="changeOption('top', -1)">←</button>
            <span id="top-text">none</span>
            <button onclick="changeOption('top', 1)">→</button>
        </div>
        <!-- Add more controls for other parameters -->
        <script>
            let options = {
                style: ['circle', 'transparent'],
                top: ['none', 'big_hair']  // Add other options for top
            };

            let currentIndex = {
                style: 0,
                top: 0
            };

            function changeOption(param, direction) {
                currentIndex[param] = (currentIndex[param] + direction + options[param].length) % options[param].length;
                document.getElementById(param + '-text').innerText = options[param][currentIndex[param]];
                updateAvatar();
            }

            function updateAvatar() {
                const style = options.style[currentIndex.style];
                const top = options.top[currentIndex.top];
                // Append other parameters as needed
                fetch(`/avatar?style=${style}&top=${top}`)  // Add other parameters in query string
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    document.getElementById('avatar-image').src = url;
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/avatar')
def avatar():
    style_key = request.args.get('style', 'circle')
    style = dict_style.get(style_key, pa.AvatarStyle.CIRCLE)
    skin_key = request.args.get('skin', 'light')
    skin = dict_skin_color.get(skin_key, pa.SkinColor.LIGHT)
    
    # Default values for other parameters (you can change these)
    background_color = "#FFFFFF"
    top_key = request.args.get('top', 'none')
    top = dict_hairstyles.get(top_key, 'no_hair')
    eyebrows = 'default'
    eyes = 'default'
    nose = 'default'
    mouth = 'default'
    facial_hair = 'none'
    skin = 'default'
    hair_color = '#000000'
    accessory = 'none'
    clothing = 'shirt'
    clothing_color = '#FF0000'

    avatar = create_avatar(style, background_color, top, eyebrows, eyes, nose, mouth, facial_hair, skin, hair_color, accessory, clothing, clothing_color)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmp_file:
        avatar.render(tmp_file.name)
        tmp_file_path = tmp_file.name

    response = send_file(tmp_file_path, mimetype='image/svg+xml')

    @response.call_on_close
    def remove_file():
        try:
            os.remove(tmp_file_path)
        except OSError:
            pass

    return response

if __name__ == '__main__':
    app.run(debug=True)
