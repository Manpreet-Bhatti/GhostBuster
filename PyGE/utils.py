import pygame
import PyGE.Globals.Constants as Constants
from xmltodict import OrderedDict

def convert_color(color:str):
    """
     Converts the string representation of a color to a valid RGB tuple
     ACCEPTABLE FORMATS (r=red, g=green, b=blue):
         - RGB FORMATS -
         (r, g, b)
         r g b
         r, g, b
         - HEX FORMATS -
         rrggbb
         #rrggbb
     :param color: the string representaion 
     :return: a valid RGB color tuple
     """

    def cmyk_to_rgb(vals:tuple):
        if type(vals) is int:
            return tuple(int(str(vals)[i:i + 2], 16) for i in (0, 2, 4))
        if len(vals) == 3:
            return vals
        if len(vals) == 4:
            c, m, y, k = vals
            rgb_scale = 255
            cmyk_scale = 100
            r = rgb_scale * (1.0 - (c + k) / float(cmyk_scale))
            g = rgb_scale * (1.0 - (m + k) / float(cmyk_scale))
            b = rgb_scale * (1.0 - (y + k) / float(cmyk_scale))
            return r, g, b

    if color in Constants.COLOR_NAMES:
        color = Constants.COLOR_NAMES[color]

    # TODO: MAKE THIS WAAAAAAAY MORE EFFICIENT
    # RGB variants
    try:
        return cmyk_to_rgb(eval(color))
    except (SyntaxError, NameError):
        try:
            return cmyk_to_rgb(eval("({})".format(",".join(color.split(" ")))))
        except (SyntaxError, NameError):
            try:
                return cmyk_to_rgb(eval("({})".format(color)))
            except (SyntaxError, NameError):
                # is it hex?
                return tuple(int(color.strip("#")[i:i + 2], 16) for i in (0, 2, 4))


def get_optional(dic: dict, key: str, default, return_type:type=None, is_literal_value=False, blank_means_unset=False):
    """
    Returns either the value in a dictionary, or a default value specified if the value is not in the dictionary
    This is a very usefull tool when working with "args" from the XML map
    :param dic: The dictionary to parse 
    :param key: The key to look for in the dictionary
    :param default: The value to return if the value does not exits
    :param return_type: The datatype to cast the result to (regardless if it is found or not)
    :param is_literal_value: If the key specified is the literal key (True), or if it should try both the value, and the value preceded by the  @ sign
    :param blank_means_unset: If a blank value is found (""), treat it as unset. Default is False
    :return: Either the value in the dictionary, or the default value
    """
    if key in dic:
        val = dic[key]
    elif "@{}".format(key) in dic and is_literal_value is False:
        val = dic["@{}".format(key)]
    else:
        val = default

    if blank_means_unset and val == "":
        return default

    if return_type is not None:
        val = return_type(val)
    if return_type is int:
        val = round(float(val), 0)
    return val


def get_mandatory(dic: dict, key: str, return_type:type=None, is_literal_value=False):
    """
    Returns the value in a dictionary. If the value does not exist, raise a ValueError
    This is a very usefull tool when working with "args" from the XML map
    :param dic: The dictionary to parse 
    :param key: The key to look for in the dictionary
    :param return_type: The datatype to cast the result to (regardless if it is found or not)
    :param is_literal_value: If the key specified is the literal key (True), or if it should try both the value, and the value preceded by the  @ sign
    :return: The value in the dictionary
    """
    if key in dic:
        val = dic[key]
    elif "@{}".format(key) in dic and is_literal_value is False:
        val = dic["@{}".format(key)]
    else:
        if type(dic) is OrderedDict:
            dic = dict(dic)
        raise ValueError("Could Not Extract Key \"{}\" From {}".format(key, dic))

    if return_type is None:
        return val
    if return_type is int:
        val = round(float(val), 0)
    return return_type(val)


def rect_a_touch_b(rect_a: tuple, rect_b: tuple):
    """
    Determines if rect_a touches rect_b (any overlap at all will return True)
    :param rect_a: The rect representation of object 1, in the format (x, y, width, height)
    :param rect_b: The rect representation of object 2, in the format (x, y, width, height)
    :return: if there is any sort of touching at all 
    """
    # if rects touch (any overlap)
    a_x, a_y, a_w, a_h = rect_a
    b_x, b_y, b_w, b_h = rect_b

    points = [
        (a_x, a_y),
        (a_x + a_w, a_y),
        (a_x + a_w, a_y + a_h),
        (a_x, a_y + a_h)
    ]

    for x, y in points:
        if b_x < x < b_x + b_w and b_y < y < b_y + b_h:
            return True
    return False


def rect_a_in_b(rect_a: tuple, rect_b: tuple):
    """
    Determines if rect_a is fully inside rect_b
    :param rect_a: The rect representation of object 1, in the format (x, y, width, height)
    :param rect_b: The rect representation of object 2, in the format (x, y, width, height)
    :return: if rect_b fully contains rect_a 
    """
    # if A is fully inside b
    a_x, a_y, a_w, a_h = rect_a
    b_x, b_y, b_w, b_h = rect_b

    points = [
        (a_x, a_y),
        (a_x + a_w, a_y),
        (a_x + a_w, a_y + a_h),
        (a_x, a_y + a_h)
    ]

    for x, y in points:
        if not (b_x < x < b_x + b_w and b_y < y < b_y + b_h):
            return False
    return True


def point_in_rect(point: tuple, rect: tuple):
    """
    Determines if a single point is inside a rectangle
    :param point: The point to check, in the format (x, y)
    :param rect: he rect representation of the rectangle, in the format (x, y, width, height)
    :return: 
    """
    x, y = point
    b_x, b_y, b_w, b_h = rect
    return b_x < x < b_x + b_w and b_y < y < b_y + b_h


def deconstruct_modifier_bitmask(modifier):
    """
    Deconstructs a keyboard modifier bitmask into a list of keyboard modifiers
    Note: the IDs are based on the Pygame keymods (ex. pygame.KMOD_RCTRL, or pygame.KMOD_CAPS)
    :param modifier: the bitmask representing the modifiers
    :return: A list of keyboar modifiers (Ex: [8192, 2] = Capslock, and Right-Shift are enabled)
    """
    modifiers = []
    mods = [
        pygame.KMOD_NONE, pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT, pygame.KMOD_LCTRL,
        pygame.KMOD_RCTRL, pygame.KMOD_CTRL, pygame.KMOD_LALT, pygame.KMOD_ALT, pygame.KMOD_LMETA, pygame.KMOD_RMETA,
        pygame.KMOD_NUM, pygame.KMOD_CAPS, pygame.KMOD_MODE
    ]
    for mod in mods:
        if modifier & mod:
            modifiers.append(mod)
    return modifiers


def scale_image(image:pygame.Surface):
    return image
    # new_h = int(round(image.get_height() * get_var("scale-factor"), 0))
    # new_w = int(round(image.get_width() * get_var("scale-factor"), 0))
    # return pygame.transform.scale(image, (new_w, new_h))

def scale_coords(coords:tuple, factor:float=None):
    if factor is None:
        # factor = get_var("scale-factor")
        return coords

    divider = 3
    coords = safe_int(coords[0] * (factor / divider)), safe_int(coords[1] * (factor / divider))
    return coords

def safe_int(val: float):
    """
    Safley casts a float to an integer by first rounding it to 0 decimal place digits
    :param val: the value to cast
    :return: an int representation of the float
    """
    return int(round(val, 0))


def center_on_screen(obj, screen):
    """
    Calculates the x and y position of "obj" to have it placed in the exact center of the screen
    :param obj: The object to center
    :param screen: The screen to center it on
    :return: The x and y position in the format (x, y)
    """
    sw, sh = screen.get_size()
    _, _, ow, oh = obj.rect

    return (sw / 2) - (ow / 2), (sh / 2) - (oh / 2)


def get_surface_center(surf: pygame.Surface):
    """
    Calculates the center point of a surface
    :param surf: the surface to calculate from
    :return: the center point as a tuple (x, y)
    """
    return surf.get_width() / 2, surf.get_height() / 2