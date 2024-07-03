import python_avatars as pa
from pymoji import *

dict_style = { 'circle': pa.AvatarStyle.CIRCLE, 'transparent': pa.AvatarStyle.TRANSPARENT, 'random': pa.AvatarStyle.pick_random()}
dict_background_color = { 'blue': '#0000FF', 'green': '#008000', 'red': '#FF0000', 'yellow': '#FFFF00', 'gray':'#808080', 'white': '#F5F5DC', 'black': '#000000', }
dict_hairstyles = {
    'none': pa.HairType.NONE,
    'big_hair': pa.HairType.BIG_HAIR,
    'bob': pa.HairType.BOB,
    'bun': pa.HairType.BUN,
    'caesar_side_part': pa.HairType.CAESAR_SIDE_PART,
    'caesar': pa.HairType.CAESAR,
    'curly': pa.HairType.CURLY,
    'curvy': pa.HairType.CURVY,
    'dreads': pa.HairType.DREADS,
    'frida': pa.HairType.FRIDA,
    'frizzle': pa.HairType.FRIZZLE,
    'fro_band': pa.HairType.FRO_BAND,
    'fro': pa.HairType.FRO,
    'long_not_too_long': pa.HairType.LONG_NOT_TOO_LONG,
    'mia_wallace': pa.HairType.MIA_WALLACE,
    'shaggy_mullet': pa.HairType.SHAGGY_MULLET,
    'shaggy': pa.HairType.SHAGGY,
    'shaved_sides': pa.HairType.SHAVED_SIDES,
    'short_curly': pa.HairType.SHORT_CURLY,
    'short_dreads_1': pa.HairType.SHORT_DREADS_1,
    'short_dreads_2': pa.HairType.SHORT_DREADS_2,
    'short_flat': pa.HairType.SHORT_FLAT,
    'short_round': pa.HairType.SHORT_ROUND,
    'short_waved': pa.HairType.SHORT_WAVED,
    'sides': pa.HairType.SIDES,
    'straight_1': pa.HairType.STRAIGHT_1,
    'straight_2': pa.HairType.STRAIGHT_2,
    'straight_strand': pa.HairType.STRAIGHT_STRAND,
    'astronout': pa.HairType.ASTRONAUT,
    'braids': pa.HairType.BRAIDS,
    'bride': pa.HairType.BRIDE,
    'buzzcut': pa.HairType.BUZZCUT,
    'cornrows': pa.HairType.CORNROWS,
    'curly_2': pa.HairType.CURLY_2,
    'dreadlocks': pa.HairType.DREADLOCKS,
    'einstein_hair': pa.HairType.EINSTEIN_HAIR,
    'elvis': pa.HairType.ELVIS,
    'evil_spike': pa.HairType.EVIL_SPIKE,
    'half_shaved': pa.HairType.HALF_SHAVED,
    'hat': pa.HairType.HAT,
    'long_hair_curly': pa.HairType.LONG_HAIR_CURLY,
    'loose_hair': pa.HairType.LOOSE_HAIR,
    'mohawk': pa.HairType.MOHAWK,
    'mowgli': pa.HairType.MOWGLI,
    'pixie': pa.HairType.PIXIE,
    'pompadour': pa.HairType.POMPADOUR,
    'quiff': pa.HairType.QUIFF,
    'twist_long_hair': pa.HairType.TWIST_LONG_HAIR,
    'twist_long_hair_2': pa.HairType.TWIST_LONG_HAIR_2,
    'wick': pa.HairType.WICK,
    'wild': pa.HairType.WILD,
    'random' : pa.HairType.pick_random()
}
# same for clothing color and hat color
dict_clothing_color = {
    'black': pa.ClothingColor.BLACK,
    'blue_01': pa.ClothingColor.BLUE_01,
    'blue_02': pa.ClothingColor.BLUE_02,
    'blue_03': pa.ClothingColor.BLUE_03,
    'gray_01': pa.ClothingColor.GRAY_01,
    'gray_02': pa.ClothingColor.GRAY_02,
    'heather': pa.ClothingColor.HEATHER,
    'pastel_blue': pa.ClothingColor.PASTEL_BLUE,
    'pastel_green': pa.ClothingColor.PASTEL_GREEN,
    'pastel_orange': pa.ClothingColor.PASTEL_ORANGE,
    'pastel_yellow': pa.ClothingColor.PASTEL_YELLOW,
    'pink': pa.ClothingColor.PINK,
    'red': pa.ClothingColor.RED,
    'white': pa.ClothingColor.WHITE,
    # 'custom': CustomColor.CUSTOM
}

dict_eyebrows = {
    'none': pa.EyebrowType.NONE,
    'angry_natural': pa.EyebrowType.ANGRY_NATURAL,
    'angry': pa.EyebrowType.ANGRY,
    'default_natural': pa.EyebrowType.DEFAULT_NATURAL,
    'default': pa.EyebrowType.DEFAULT,
    'flat_natural': pa.EyebrowType.FLAT_NATURAL,
    'frown_natural': pa.EyebrowType.FROWN_NATURAL,
    'raised_excited_natural': pa.EyebrowType.RAISED_EXCITED_NATURAL,
    'raised_excited': pa.EyebrowType.RAISED_EXCITED,
    'sad_concerned_natural': pa.EyebrowType.SAD_CONCERNED_NATURAL,
    'sad_concerned': pa.EyebrowType.SAD_CONCERNED,
    'unibrow_natural': pa.EyebrowType.UNIBROW_NATURAL,
    'up_down_natural': pa.EyebrowType.UP_DOWN_NATURAL,
    'up_down': pa.EyebrowType.UP_DOWN,
    'random': pa.EyebrowType.pick_random()
}

dict_eyes = {
    'close': pa.EyeType.CLOSED,
    'cry': pa.EyeType.CRY,
    'default': pa.EyeType.DEFAULT,
    'eye_roll': pa.EyeType.EYE_ROLL,
    'happy': pa.EyeType.HAPPY,
    'heart': pa.EyeType.HEART,
    'side': pa.EyeType.SIDE,
    'squint': pa.EyeType.SQUINT,
    'surprised': pa.EyeType.SURPRISED,
    'wink_wacky': pa.EyeType.WINK_WACKY,
    'wink': pa.EyeType.WINK,
    'x_dizzy': pa.EyeType.X_DIZZY,
    'random': pa.EyeType.pick_random()
}

dict_nose = {
    'default': pa.NoseType.DEFAULT,
    'small': pa.NoseType.SMALL,
    'wide': pa.NoseType.WIDE,
    'random': pa.NoseType.pick_random()
}

dict_mouth = {
    'concerned': pa.MouthType.CONCERNED,
    'default': pa.MouthType.DEFAULT,
    'disbelief': pa.MouthType.DISBELIEF,
    'eating': pa.MouthType.EATING,
    'grimace': pa.MouthType.GRIMACE,
    'sad': pa.MouthType.SAD,
    'scream_open': pa.MouthType.SCREAM_OPEN,
    'serious': pa.MouthType.SERIOUS,
    'smile': pa.MouthType.SMILE,
    'tongue': pa.MouthType.TONGUE,
    'twinkle': pa.MouthType.TWINKLE,
    'vomit': pa.MouthType.VOMIT,
    'big_smile': pa.MouthType.BIG_SMILE,
    'random': pa.MouthType.pick_random()
}

dict_facial_hair = {
    'none': pa.FacialHairType.NONE,
    'beard_light': pa.FacialHairType.BEARD_LIGHT,
    'beard_magestic': pa.FacialHairType.BEARD_MAGESTIC,
    'beard_medium': pa.FacialHairType.BEARD_MEDIUM,
    'moustache_fancy': pa.FacialHairType.MOUSTACHE_FANCY,
    'moustache_magnum': pa.FacialHairType.MOUSTACHE_MAGNUM,
    'einstein_moustache': pa.FacialHairType.EINSTEIN_MOUSTACHE,
    'wick_beard': pa.FacialHairType.WICK_BEARD,
    'random': pa.FacialHairType.pick_random()
}

dict_skin_color = {
    'tanned': pa.SkinColor.TANNED,
    'yellow': pa.SkinColor.YELLOW,
    'pale': pa.SkinColor.PALE,
    'light': pa.SkinColor.LIGHT,
    'brown': pa.SkinColor.BROWN,
    'dark_brown': pa.SkinColor.DARK_BROWN,
    'black': pa.SkinColor.BLACK,
    # 'custom': CustomColor.CUSTOM
}

#same for hair and facial hair
dict_hair_color = {
    'auburn': pa.HairColor.AUBURN,
    'black': pa.HairColor.BLACK,
    'blonde': pa.HairColor.BLONDE,
    'blonde_golden': pa.HairColor.BLONDE_GOLDEN,
    'brown': pa.HairColor.BROWN,
    'brown_dark': pa.HairColor.BROWN_DARK,
    'pastel_pink': pa.HairColor.PASTEL_PINK,
    'platinum': pa.HairColor.PLATINUM,
    'red': pa.HairColor.RED,
    'silver_gray': pa.HairColor.SILVER_GRAY,
    # 'custom': CustomColor.CUSTOM
}

dict_accessory = {
    'none': pa.AccessoryType.NONE,
    'eyepatch': pa.AccessoryType.EYEPATCH,
    'kurt': pa.AccessoryType.KURT,
    'prescription_1': pa.AccessoryType.PRESCRIPTION_1,
    'prescription_2': pa.AccessoryType.PRESCRIPTION_2,
    'round': pa.AccessoryType.ROUND,
    'sunglasses': pa.AccessoryType.SUNGLASSES,
    'wayfarers': pa.AccessoryType.WAYFARERS,
    'sunglasses_2': pa.AccessoryType.SUNGLASSES_2,
    'wayfarers_2': pa.AccessoryType.WAYFARERS_2,
    'random': pa.AccessoryType.pick_random()
}

dict_clothing_types = {
    'none': pa.ClothingType.NONE,
    'blazer_shirt': pa.ClothingType.BLAZER_SHIRT,
    'blazer_sweater': pa.ClothingType.BLAZER_SWEATER,
    'collar_sweater': pa.ClothingType.COLLAR_SWEATER,
    'graphic_shirt': pa.ClothingType.GRAPHIC_SHIRT,
    'hoodie': pa.ClothingType.HOODIE,
    'overall': pa.ClothingType.OVERALL,
    'shirt_crew_neck': pa.ClothingType.SHIRT_CREW_NECK,
    'shirt_scoop_neck': pa.ClothingType.SHIRT_SCOOP_NECK,
    'shirt_v_neck': pa.ClothingType.SHIRT_V_NECK,
    'astronaut_suit': pa.ClothingType.ASTRONAUT_SUIT,
    'bond_suit': pa.ClothingType.BOND_SUIT,
    'chef': pa.ClothingType.CHEF,
    'gladiator': pa.ClothingType.GLADIATOR,
    'jedi_robe': pa.ClothingType.JEDI_ROBE,
    'shirt_wick': pa.ClothingType.SHIRT_WICK,
    'random': pa.ClothingType.pick_random()
}

dict_clothing_graphics = {
    'none': pa.ClothingGraphic.NONE,
    'bat': pa.ClothingGraphic.BAT,
    'bear': pa.ClothingGraphic.BEAR,
    'cumbia': pa.ClothingGraphic.CUMBIA,
    'custom_text': pa.ClothingGraphic.CUSTOM_TEXT,
    'deer': pa.ClothingGraphic.DEER,
    'diamond': pa.ClothingGraphic.DIAMOND,
    'hola': pa.ClothingGraphic.HOLA,
    'pizza': pa.ClothingGraphic.PIZZA,
    'resist': pa.ClothingGraphic.RESIST,
    'selena': pa.ClothingGraphic.SELENA,
    'skull_outline': pa.ClothingGraphic.SKULL_OUTLINE,
    'skull': pa.ClothingGraphic.SKULL
}