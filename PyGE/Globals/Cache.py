import os
import pygame

from PyGE.Misc.Font import Font
from PyGE.Misc.SpriteSheet import SpriteSheet
from PyGE.Misc.Video import Video
from PyGE.Misc.Model import Model
from PyGE.utils import scale_image

# cache dictionaries
images = {}         # image cache
spritesheets = {}   # spritesheet cache
sounds = {}         # sound cache
font = {}
image_paths = {}
sound_paths = {}
vector_graphic = {}
videos = {}
models = {}
subrooms = {}


DEFAULT_IMAGE = None            # The default image (MUST BE STORED IN THE CACHE!)
DEFAULT_SPRITE_SHEET = None     # The default spritesheet (MUST BE STORED IN THE CACHE!)


def set_default_image(name):
    """
    Sets the image (which must be stored in the image cache) which will be used in the event an image can not be found in the cache
    Set to 'None' to have an exception thrown instead of use a default image
    :param name: the name of the image in the image cache
    """
    global DEFAULT_IMAGE
    DEFAULT_IMAGE = name


def set_default_spritesheet(name):
    """
    Sets the spritesheet (which must be stored in the spritesheet cache) which will be used in the event an spritesheet can not be found in the cache
    Set to 'None' to have an exception thrown instead of use a default spritesheet
    :param name: the name of the spritesheet in the spritesheet cache
    """
    global DEFAULT_SPRITE_SHEET
    DEFAULT_SPRITE_SHEET = name


def set_image(name, path, width=None, height=None):
    """
    Loads a single image into the image cache 
    :param name: The name to save the image in the cache as
    :param path: The path to the image save location
    :param width: The new width of the image
    :param height: The new height of the image
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("The File You Have Requested '{}' Could Not Be Located. Please Check The Path, And Ensure The File Exists.".format(path))
    img = pygame.image.load(path)
    if width is None:
        width = img.get_width()
    if height is None:
        height = img.get_height()
    image_paths[name] = path
    images[name] = scale_image(pygame.transform.scale(img, (width, height)))


def get_image(name):
    """
    Gets the image from the cache by it's name
    :param name: The name of the image
    :return: The image from the cache
    """
    if name not in images and DEFAULT_IMAGE is not None:
        return images[DEFAULT_IMAGE]
    return images[name]


def cache_image_dir(dir_path:str, scale:float=1.0):
    """
    Loads every image from a directory into the cache.
    NOTE: The name of each image, is the image's file name without the extension
    NOTE: Will NOT check subdirectories.
    :param dir_path: The path to the directory of the files
    :param scale: The factor to multiply the image size by (Ex: 2 doubles the size, and 0.5 halves the size)
    """
    for name in os.listdir(dir_path):
        path = os.path.join(dir_path, name)
        if os.path.isdir(path):
            continue

        name = name[:name.index(".")]
        image = pygame.image.load(path)
        new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.scale(image, new_size)
        images[name] = image


def get_image_cache_list():
    """
    Formats the image in a list format. Each item in the list is a dictionary object in the format:
    {"name": "image_reference_name", "path": "path_to_localy_saved_image", "w": "width_of_image", "h": "height_of_image"}
    :return: the list of dictionaries describing each image in the cache
    """
    out = []
    for name, image in images.items():
        w, h = image.get_size()
        out.append({
            "name": name,
            "path": image_paths[name],
            "w": w,
            "h": h
        })
    return out


def get_image_paths():
    """
    Returns the reference name of each image in the cache, and the path in a dictionary format
    :return: the dictionary of names and paths
    """
    return image_paths


def clear_image_cache():
    """
    Clears the entire image cache
    (WARNING: Don't forget to add images back to the cache before referencing them)
    """
    global images
    global image_paths
    image_paths = {}
    images = {}


def set_spritesheet(name, image:str, w:int, h:int, duration:float=None, final_size:tuple=None, invisible_color:tuple=(0, 0, 1)):
    """
    Loads a spritesheet into the spritesheet cache
    :param name: The name to save the spritesheet under
    :param image: The path to the spritesheet
    :param w: The number of columns the spritesheet contains
    :param h: The number of rows the spritesheet contains
    :param duration: The length of time to stay on each frame
    :param final_size: The size to scale each frame to in the format (width, height)
    :param invisible_color: Some RGB color which will be ignored. (in general, select a color not in any of the images)
    """
    if not os.path.isfile(image):
        raise FileNotFoundError("The File You Have Requested '{}' Could Not Be Located. Please Check The Path, And Ensure The File Exists.".format(image))
    spritesheets[name] = SpriteSheet(image, w, h, duration, final_size, invisible_color)


def get_spritesheet(name):
    """
    Gets a spritesheet from the cache based on the name
    :param name: The name of the spritesheet
    :return: The spritesheet with the specified name
    """
    if name not in spritesheets and DEFAULT_SPRITE_SHEET is not None:
        return spritesheets[DEFAULT_SPRITE_SHEET]
    return spritesheets[name]


def get_spritesheet_cache_list():
    """
    Formats the sprite sheets in a list format. Each item in the list is a dictionary object
    :return: the list of dictionaries describing each spritesheet in the cache
    """
    out = []
    for name, ss in spritesheets.items():   #type: str, SpriteSheet
        out.append({
            "name": name,
            "path": ss.path,
            "w": ss.w,
            "h": ss.h,
            "duration": ss.duration,
            "final_size": ss.final_size,
            "invisible_color": ss.invisible_color
        })
    return out


def clear_spritesheet_cache():
    """
    Clears the entire spritesheet cache
    (WARNING: Don't forget to add spritesheets back to the cache before referencing them)
    """
    global spritesheets
    spritesheets = {}


def set_sound(name:str, path:str, volume:float=1):
    """
    Loads a sound file into the cache based on the name
    :param name: The name to save the sound under
    :param path: The path of the sound
    :param volume: The volume to play the sound at (1 = Full, 0 = Mute)
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("The File You Have Requested '{}' Could Not Be Located. Please Check The Path, And Ensure The File Exists.".format(path))
    sounds[name] = pygame.mixer.Sound(path)
    sounds[name].set_volume(volume)
    sound_paths[name] = path


def get_sound(name):
    """
    Gets the sound from the cache based on the name
    :param name: The name of the sound
    :return: The sound with the specified name
    """
    return sounds[name]


def clear_sound_cache():
    """
    Clears the entire sound cache
    (WARNING: Don't forget to add sounds back to the cache before referencing them)
    """
    global sounds
    global sound_paths
    sounds = {}
    sound_paths = {}


def get_sound_cache_list():
    """
    Formats the sounds in a list format. Each item in the list is a dictionary object
    :return: the list of dictionaries describing each sound in the cache
    """
    out = []
    for name, s in sounds.items():   #type: str, Sound
        out.append({
            "name": name,
            "path": sound_paths[name],
            "volume": s.get_volume()
        })
    return out


def set_font(name:str, path:str, size:int, bold:bool=False, italic:bool=False):
    """
    Loads a font into the font cache based on the name
    :param name: the name to save the font under (Recomended convention is [fontname][size]. Ex. Arial12, or CourierNew15)
    :param path: the path to the .ttf/.otf file. A system font can be used, however, it HIGHLY discouraged as it WILL cause a fatal error when the project is exported
    :param size: the size of the font (in pt) 
    :param bold: if the font should be bolded (default is False)
    :param italic: if the font should be italicised (default is False)
    """
    font[name] = Font(path, size, bold=bold, italic=italic)


def get_font(name):
    """
    Retrurns the font in the cache with the specified name
    :param name: the name of the font
    :return: the font assigned to the provided name
    """
    return font[name]


def clear_font_cache():
    """
    Clears the entire font cache
    (WARNING: Don't forget to add fonts back to the cache before referencing them)
    """
    global font
    font = {}


def get_font_cache_list():
    """
    Formats the fonts in a list format. Each item in the list is a dictionary object
    :return: the list of dictionaries describing each font in the cache
    """
    out = []
    for name, f in font.items():   #type: str, Font
        out.append({
            "name": name,
            "path": f.path,
            "size": f.size
        })
    return out


def set_video(name, path, has_mask=False, audio=True, audio_buffersize=200000, target_resolution=None,
            resize_algorithm='bicubic', audio_fps=44100, audio_nbytes=2, verbose=False, fps_source='tbr'):
    """
    Loads a video into cache
    :param name: the name of the video
    :param path: the path to the video
    :param has_mask: If the video should contain a mask (rarley used)
    :param audio: If the video should play it's audio
    :param audio_buffersize: 
    :param target_resolution: the size to set the video to (default is the screen size)
    :param resize_algorithm: The algorithm to resize the video ("bicubic", "bilinear", or "fast_bilinear")
    :param audio_fps: 
    :param audio_nbytes: 
    :param verbose: 
    :param fps_source: 
    """

    if target_resolution is not None:
        target_resolution = (target_resolution[1], target_resolution[0])
    videos[name] = Video(
        path, has_mask, audio, audio_buffersize, target_resolution, resize_algorithm, audio_fps, audio_nbytes,
        verbose, fps_source
    )


def get_video(name):
    """
    Retrurns the video in the cache with the specified name
    :param name: the name of the video
    :return: the video assigned to the provided name
    """
    return videos[name]


def set_model(name, path):
    models[name] = Model(path)


def set_subroom(name, subroom):
    """
    Loads a subroom into cache
    :param name: the reference name of the subroom
    :param subroom: the subroom object
    """
    subrooms[name] = subroom