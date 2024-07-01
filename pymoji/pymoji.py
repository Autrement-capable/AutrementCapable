import python_avatars as pa

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

# Save to a file
def save_avatar(avatar, filename):
    avatar.render(filename)