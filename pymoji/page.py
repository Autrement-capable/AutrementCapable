from flask import Flask, send_file, render_template_string, request, jsonify, send_from_directory
import io
import python_avatars as pa
from pymoji import avatar_from_username
from dictionaries import *
import tempfile
import os
import random

app = Flask(__name__, static_folder='avatar-generator/dist', static_url_path='')

# Dictionaries to handle different avatar parameters
# dict_style = { 'circle': pa.AvatarStyle.CIRCLE, 'transparent': pa.AvatarStyle.TRANSPARENT }
style_keys = list(dict_style.keys())
backgorund_color_keys = list(dict_background_color.keys())
hairstyle_keys = list(dict_hairstyles.keys())
clothing_color_keys = list(dict_clothing_color.keys())
eyebrows_keys = list(dict_eyebrows.keys())
eyes_keys = list(dict_eyes.keys())
nose_keys = list(dict_nose.keys())
mouth_keys = list(dict_mouth.keys())
facial_hair_keys = list(dict_facial_hair.keys())
skin_color_keys = list(dict_skin_color.keys())
hair_color_keys = list(dict_hair_color.keys())
accessory_keys = list(dict_accessory.keys())
clothing_keys = list(dict_clothing_types.keys())
dict_clothing_graphics_keys = list(dict_clothing_graphics.keys())


# def get_really_random_avatar():
#     return pa.Avatar.random()

# Function to generate a random avatar
def random_avatar(style='random', background_color='random', hairstyle='random', clothing_color='random', eyebrows='random', eyes='random', nose='random', mouth='random', facial_hair='random', skin='random', hair_color='random', accessory='random', clothing='random', clothing_graphics='random'):
    avatar_style = dict_style.get(style, pa.AvatarStyle.pick_random())
    background_color = dict_background_color.get(background_color, pa.BackgroundColor.pick_random())
    top = dict_hairstyles.get(hairstyle, pa.TopType.pick_random())
    clothing_color = dict_clothing_color.get(clothing_color, pa.ClothingColor.pick_random())
    eyebrows = dict_eyebrows.get(eyebrows, pa.EyebrowType.pick_random())
    eyes = dict_eyes.get(eyes, pa.EyeType.pick_random())
    nose = dict_nose.get(nose, pa.NoseType.pick_random())
    mouth = dict_mouth.get(mouth, pa.MouthType.pick_random())
    facial_hair = dict_facial_hair.get(facial_hair, pa.FacialHairType.pick_random())
    skin_color = dict_skin_color.get(skin, pa.SkinColor.pick_random())
    hair_color = dict_hair_color.get(hair_color, pa.HairColor.pick_random())
    accessory = dict_accessory.get(accessory, pa.AccessoryType.pick_random())
    clothing = dict_clothing_types.get(clothing, pa.ClothingType.pick_random())
    clothing_graphics = dict_clothing_graphics.get(clothing_graphics, pa.ClothingGraphic.pick_random())
    return pa.Avatar(style=avatar_style, background_color=background_color, top=top, eyebrows=eyebrows, eyes=eyes, nose=nose, mouth=mouth, facial_hair=facial_hair, skin_color = skin_color, hair_color=hair_color, accessory=accessory, clothing=clothing, shirt_graphic=clothing_graphics, clothing_color=clothing_color)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)



@app.route('/really_random_avatar')
def really_random_avatar():
    avatar = pa.Avatar.random()
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


@app.route('/avatar')
def avatar():
    avatar = random_avatar()
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

@app.route('/avatar/<username>')
def avatar_from_user(username):
    avatar = avatar_from_username(username)
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

# To keep track of the current style index
current_style_index = 0
current_background_color_index = 0
current_hairstyle_index = 0
current_clothing_color_index = 0
current_eyebrows_index = 0
current_eyes_index = 0
current_nose_index = 0
current_mouth_index = 0
current_facial_hair_index = 0
current_skin_color_index = 0
current_hair_color_index = 0
current_accessory_index = 0
current_clothing_index = 0
current_clothing_graphics_index = 0
current_hat_color_index = 0

@app.route('/avatar/update')
def update_avatar():
    global current_style_index
    global current_background_color_index
    global current_hairstyle_index
    global current_clothing_color_index
    global current_eyebrows_index
    global current_eyes_index
    global current_nose_index
    global current_mouth_index
    global current_facial_hair_index
    global current_skin_color_index
    global current_hair_color_index
    global current_accessory_index
    global current_clothing_index
    global current_clothing_graphics_index
    global current_hat_color_index

    param = request.args.get('param')
    direction = request.args.get('direction')

    if param == 'style':
        if direction == 'next':
            current_style_index = (current_style_index + 1) % len(style_keys)
        elif direction == 'prev':
            current_style_index = (current_style_index - 1) % len(style_keys)
    if param == 'background_color':
        if direction == 'next':
            current_background_color_index = (current_background_color_index + 1) % len(backgorund_color_keys)
        elif direction == 'prev':
            current_background_color_index = (current_background_color_index - 1) % len(backgorund_color_keys)
    if param == 'hairstyle':
        if direction == 'next':
            current_hairstyle_index = (current_hairstyle_index + 1) % len(hairstyle_keys)
        elif direction == 'prev':
            current_hairstyle_index = (current_hairstyle_index - 1) % len(hairstyle_keys)
    if param == 'clothing_color':
        if direction == 'next':
            current_clothing_color_index = (current_clothing_color_index + 1) % len(clothing_color_keys)
        elif direction == 'prev':
            current_clothing_color_index = (current_clothing_color_index - 1) % len(clothing_color_keys)
    if param == 'eyebrows':
        if direction == 'next':
            current_eyebrows_index = (current_eyebrows_index + 1) % len(eyebrows_keys)
        elif direction == 'prev':
            current_eyebrows_index = (current_eyebrows_index - 1) % len(eyebrows_keys)
    if param == 'eyes':
        if direction == 'next':
            current_eyes_index = (current_eyes_index + 1) % len(eyes_keys)
        elif direction == 'prev':
            current_eyes_index = (current_eyes_index - 1) % len(eyes_keys)
    if param == 'nose':
        if direction == 'next':
            current_nose_index = (current_nose_index + 1) % len(nose_keys)
        elif direction == 'prev':
            current_nose_index = (current_nose_index - 1) % len(nose_keys)
    if param == 'mouth':
        if direction == 'next':
            current_mouth_index = (current_mouth_index + 1) % len(mouth_keys)
        elif direction == 'prev':
            current_mouth_index = (current_mouth_index - 1) % len(mouth_keys)
    if param == 'facial_hair':
        if direction == 'next':
            current_facial_hair_index = (current_facial_hair_index + 1) % len(facial_hair_keys)
        elif direction == 'prev':
            current_facial_hair_index = (current_facial_hair_index - 1) % len(facial_hair_keys)
    if param == 'skin_color':
        if direction == 'next':
            current_skin_color_index = (current_skin_color_index + 1) % len(skin_color_keys)
        elif direction == 'prev':
            current_skin_color_index = (current_skin_color_index - 1) % len(skin_color_keys)
    if param == 'hair_color':
        if direction == 'next':
            current_hair_color_index = (current_hair_color_index + 1) % len(hair_color_keys)
        elif direction == 'prev':
            current_hair_color_index = (current_hair_color_index - 1) % len(hair_color_keys)
    if param == 'accessory':
        if direction == 'next':
            current_accessory_index = (current_accessory_index + 1) % len(accessory_keys)
        elif direction == 'prev':
            current_accessory_index = (current_accessory_index - 1) % len(accessory_keys)
    if param == 'clothing':
        if direction == 'next':
            current_clothing_index = (current_clothing_index + 1) % len(clothing_keys)
        elif direction == 'prev':
            current_clothing_index = (current_clothing_index - 1) % len(clothing_keys)
    if param == 'clothing_graphics':
        if direction == 'next':
            current_clothing_graphics_index = (current_clothing_graphics_index + 1) % len(dict_clothing_graphics_keys)
        elif direction == 'prev':
            current_clothing_graphics_index = (current_clothing_graphics_index - 1) % len(dict_clothing_graphics_keys)
    if param == 'random':
        if direction == 'none':
            current_style_index = random.randint(0, len(style_keys) - 1)
            current_background_color_index = random.randint(0, len(backgorund_color_keys) - 1)
            current_hairstyle_index = random.randint(0, len(hairstyle_keys) - 1)
            current_clothing_color_index = random.randint(0, len(clothing_color_keys) - 1)
            current_eyebrows_index = random.randint(0, len(eyebrows_keys) - 1)
            current_eyes_index = random.randint(0, len(eyes_keys) - 1)
            current_nose_index = random.randint(0, len(nose_keys) - 1)
            current_mouth_index = random.randint(0, len(mouth_keys) - 1)
            current_facial_hair_index = random.randint(0, len(facial_hair_keys) - 1)
            current_skin_color_index = random.randint(0, len(skin_color_keys) - 1)
            current_hair_color_index = random.randint(0, len(hair_color_keys) - 1)
            current_accessory_index = random.randint(0, len(accessory_keys) - 1)
            current_clothing_index = random.randint(0, len(clothing_keys) - 1)
            current_clothing_graphics_index = random.randint(0, len(dict_clothing_graphics_keys) - 1)
    
    selected_style = style_keys[current_style_index]
    selected_background_color = backgorund_color_keys[current_background_color_index]
    selected_hairstyle = hairstyle_keys[current_hairstyle_index]
    selected_clothing_color = clothing_color_keys[current_clothing_color_index]
    selected_eyebrows = eyebrows_keys[current_eyebrows_index]
    selected_eyes = eyes_keys[current_eyes_index]
    selected_nose = nose_keys[current_nose_index]
    selected_mouth = mouth_keys[current_mouth_index]
    selected_facial_hair = facial_hair_keys[current_facial_hair_index]
    selected_skin_color = skin_color_keys[current_skin_color_index]
    selected_hair_color = hair_color_keys[current_hair_color_index]
    selected_accessory = accessory_keys[current_accessory_index]
    selected_clothing = clothing_keys[current_clothing_index]
    selected_clothing_graphics = dict_clothing_graphics_keys[current_clothing_graphics_index]
    # selected_hat_color = clothing_color_keys[current_hat_color_index]
    avatar = random_avatar(style=selected_style, background_color=selected_background_color, hairstyle=selected_hairstyle, clothing_color=selected_clothing_color, eyebrows=selected_eyebrows, eyes=selected_eyes, nose=selected_nose, mouth=selected_mouth, facial_hair=selected_facial_hair, skin=selected_skin_color, hair_color=selected_hair_color, accessory=selected_accessory, clothing=selected_clothing, clothing_graphics=selected_clothing_graphics)
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
