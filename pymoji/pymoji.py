import python_avatars as pa
from dictionaries import *


def random_avatar():
    return pa.Avatar.random()


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
        skin = skin,
        hair_color=hair_color,
        accessory=accessory,
        clothing=clothing,
        clothing_color=clothing_color
    )


def get_nth_enum_item(n, e):
    items = e.get_all()
    return items[n % len(items)]

def avatar_from_username(username):
    username_hash = hash(username)

    return pa.Avatar(
        style=get_nth_enum_item(username_hash, pa.AvatarStyle),
        background_color=get_nth_enum_item(username_hash, pa.BackgroundColor),
        top=get_nth_enum_item(username_hash, pa.TopType),
        hat_color=get_nth_enum_item(username_hash, pa.ClothingColor),
        eyebrows=get_nth_enum_item(username_hash, pa.EyebrowType),
        eyes=get_nth_enum_item(username_hash, pa.EyeType),
        nose=get_nth_enum_item(username_hash, pa.NoseType),
        mouth=get_nth_enum_item(username_hash, pa.MouthType),
        facial_hair=get_nth_enum_item(username_hash, pa.FacialHairType),
        skin_color=get_nth_enum_item(username_hash, pa.SkinColor),
        hair_color=get_nth_enum_item(username_hash, pa.HairColor),
        facial_hair_color=get_nth_enum_item(username_hash, pa.HairColor),
        accessory=get_nth_enum_item(username_hash, pa.AccessoryType),
        clothing=get_nth_enum_item(username_hash, pa.ClothingType),
        clothing_color=get_nth_enum_item(username_hash, pa.ClothingColor),
        shirt_graphic=get_nth_enum_item(username_hash, pa.ClothingGraphic),
        shirt_text=username,
        title=f"Avatar for {username}",
    )

# Save to a file
def save_avatar(avatar, filename):
    avatar.render(filename)