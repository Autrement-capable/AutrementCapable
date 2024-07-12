import python_avatars as pa
import hashlib
from Avatar_gen.dictionaries import *
from random import Random

def get_hash_with_salt(input_string, salt):
    """Generate a hash for the input string combined with a salt."""
    combined = input_string + salt
    return int(hashlib.sha256(combined.encode('utf-8')).hexdigest(), 16)


def Inc(index_dict, attr):
    index_dict[attr] = (index_dict[attr] + 1) % len(globals()[f"list_{attr}"])

def Dec(index_dict, attr):
    index_dict[attr] = (index_dict[attr] - 1) % len(globals()[f"list_{attr}"])

def Rand(index_dict, attr):
    index_dict[attr] = Random.randint(0, len(globals()[f"list_{attr}"]) - 1)

def Reset(index_dict, attr):
    index_dict[attr] = get_hash_with_salt(index_dict["username"], attr) % len(globals()[f"list_{attr}"])

action_types = { "inc" : Inc , "dec" : Dec, "rand" : Rand, "reset" : Reset }

# all the pa.Avatar are params of this function
def create_avatar(style, background_color, top, eyebrows, eyes, nose, mouth, facial_hair, skin_color, hair_color, accessory, clothing_type, clothing_color,
                    clothing_graphics, title):

    return pa.Avatar( style=style,
        background_color=background_color,
        top=top,
        eyebrows=eyebrows,
        hat_color=clothing_color,
        eyes=eyes,
        nose=nose,
        mouth=mouth,
        facial_hair=facial_hair,
        skin_color=skin_color,
        hair_color=hair_color,
        accessory=accessory,
        clothing=clothing_type,
        clothing_color=clothing_color,
        shirt_graphic= clothing_graphics,
        title=title + "'s Avatar",
        shirt_text=title
    )

def get_nth_list_item(n, lst):
    """Get the nth item from a list and return the item and the index.
    Ensures that the index is within the range of the list."""
    index = n % len(lst)
    return lst[index], index


def avatar_from_username(username):
    style, style_index = get_nth_list_item(get_hash_with_salt(username, 'style'), list_styles)
    background_color, background_color_index = get_nth_list_item(get_hash_with_salt(username, 'background_color'), list_background_color)
    top, top_index = get_nth_list_item(get_hash_with_salt(username, 'top'), list_hairstyles)
    clothing_color, clothing_color_index = get_nth_list_item(get_hash_with_salt(username, 'clothing_color'), list_clothing_color)
    eyebrows, eyebrows_index = get_nth_list_item(get_hash_with_salt(username, 'eyebrows'), list_eyebrows)
    eyes, eyes_index = get_nth_list_item(get_hash_with_salt(username, 'eyes'), list_eyes)
    nose, nose_index = get_nth_list_item(get_hash_with_salt(username, 'nose'), list_nose)
    mouth, mouth_index = get_nth_list_item(get_hash_with_salt(username, 'mouth'), list_mouth)
    facial_hair, facial_hair_index = get_nth_list_item(get_hash_with_salt(username, 'facial_hair'), list_facial_hair)
    skin_color, skin_color_index = get_nth_list_item(get_hash_with_salt(username, 'skin_color'), list_skin_color)
    hair_color, hair_color_index = get_nth_list_item(get_hash_with_salt(username, 'hair_color'), list_hair_color)
    accessory, accessory_index = get_nth_list_item(get_hash_with_salt(username, 'accessory'), list_accessory)
    clothing_types, clothing_types_index = get_nth_list_item(get_hash_with_salt(username, 'clothing_types'), list_clothing_types)
    clothing_graphics, clothing_graphics_index = get_nth_list_item(get_hash_with_salt(username, 'clothing_graphics'), list_clothing_graphics)

    index_dict = {
        "styles" : style_index,
        "background_colors" : background_color_index,
        "hairstyles" : top_index,
        "clothing_color" : clothing_color_index,
        "eyebrows" : eyebrows_index,
        "eyes" : eyes_index,
        "nose" : nose_index,
        "mouth" : mouth_index,
        "facial_hair" : facial_hair_index,
        "skin_color" : skin_color_index,
        "hair_color" : hair_color_index,
        "accessory" : accessory_index,
        "clothing_types" : clothing_types_index,
        "clothing_graphics" : clothing_graphics_index,
        "username" : username,
    }

    return create_avatar(
        style, background_color, top, eyebrows,
        eyes, nose, mouth, facial_hair, skin_color,
        hair_color, accessory, clothing_types, clothing_color,
        clothing_graphics, username), index_dict

def regenerate_avatar(index_dict:dict, action_type, attr):
    if attr not in example_dict_index.keys():
        return None
    try:
        action_types[action_type](index_dict, attr)
    except KeyError:
        # Foul play detected
        return None
    return create_avatar(
        list_styles[index_dict["styles"]],
        list_background_color[index_dict["background_colors"]],
        list_hairstyles[index_dict["hairstyles"]],
        list_eyebrows[index_dict["eyebrows"]],
        list_eyes[index_dict["eyes"]],
        list_nose[index_dict["nose"]],
        list_mouth[index_dict["mouth"]],
        list_facial_hair[index_dict["facial_hair"]],
        list_skin_color[index_dict["skin_color"]],
        list_hair_color[index_dict["hair_color"]],
        list_accessory[index_dict["accessory"]],
        list_clothing_types[index_dict["clothing_types"]],
        list_clothing_color[index_dict["clothing_color"]],
        list_clothing_graphics[index_dict["clothing_graphics"]],
        index_dict["username"]), index_dict

# Save to a file
def save_avatar(avatar, filename):
    avatar.render(filename)

__all__ = ["random_avatar", "create_avatar", "avatar_from_username", "save_avatar", "regenerate_avatar"]