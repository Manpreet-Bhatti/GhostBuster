import logging
import threading
import time
import typing

import pygame

from PyGE.Globals.Cache import set_spritesheet, set_image, set_sound, set_default_image, set_default_spritesheet, \
    set_font, set_video, set_model
from PyGE.Globals.GlobalVariable import set_var, set_sys_var
from PyGE.Misc.Computer import get_monitor_resolution
from PyGE.PyGEObject import PyGE
from PyGE.utils import get_optional

LM_XML = 0
LM_JSON = 1


def side_scroller(xml:str, start_room:str, images=None, sprite_sheets=None, sounds=None, font=None, videos=None, development_screen_size:tuple=None, refresh_rate:int=60,
        caption:str= "Python Side Scroller Engine", icon:str=None, loading_screen:callable=None, min_loading_time:int=0,
        custom_objects:typing.List=None, enable_alt_f4:bool=True, initial_variables=None, fullscreen:bool=True,
        debug:bool=False, debug_color:tuple=(255, 255, 255), auto_scale:bool=True, default_image:str=None,
        default_spritesheet:str=None, post_load:callable=None, alt_side_scroller=None, background_color:tuple=(0, 0, 0)
):

    logging.warning("The Calling Of The 'side_scroller' Will Soon Be Depricated. Please Call The New 'pyge_application' Function Instead")

    return pyge_application(xml, start_room, images, sprite_sheets, sounds, font, videos, None, development_screen_size, refresh_rate,
        caption, icon, loading_screen, min_loading_time,
        custom_objects, enable_alt_f4, initial_variables, fullscreen,
        debug, debug_color, auto_scale, default_image,
        default_spritesheet, post_load, alt_side_scroller, background_color)

def pyge_application(
        level_data:str, start_room:str, images=None, sprite_sheets=None, sounds=None, font=None, videos=None,
        models=None, development_screen_size:tuple=None, refresh_rate:int=60,
        caption:str= "Python Game Engine Application", icon:str=None, loading_screen:callable=None,
        min_loading_time:int=0, custom_objects:list=None, enable_alt_f4:bool=True, initial_variables=None,
        fullscreen:bool=True, debug:bool=False, debug_color:tuple=(255, 255, 255), auto_scale:bool=True,
        default_image:str=None, default_spritesheet:str=None, post_load:callable=None, alt_side_scroller=None,
        background_color:tuple=(0, 0, 0), load_mode:int=0, audio_anaylasis_enabled:bool=False
):
    """
    This is the function which starts the engine.
    This is the single most important function in the entire system.
    :param level_data: The XML data to build the game from
    :param start_room: The name of the room to start the player in
    :param images: A dictionary of the images, and their names to pre-load into the image cache. The value must be a dict object. Use "path" to specify the path to the image, "w" to specify the width to scale the image to (optional) and "h" to specify the height to scale the image to (optional)
    :param sprite_sheets: A dictionary of the Sprite Sheets, and their names to pre-load into the Sprite Sheets cache. Use "path" to specify the path to the sheet, "w" to specify the number of rows are in the sheet, "h" to specify the number of cols that are in the sheet, "duration" to specify the length of time to stay on each image, final_size as the size to scale each image to (format: [width, height]), and "invisible_color" as some RGB color which will be ignored. (in general, select a color not in any of the images)
    :param sounds: A dictionary of the sounds and their names to pre-load to the sound cache. Use "path" to specify the path to the sound, "volume" to specify the volume to play the sound at
    :param font: A dictionary of the fonts and their names to pre-load to the font cache. Use "path" to specify the path to the font, "size" to specify the font size, "bold" to specify if the font should be bold (default is False), and "italic" to specify if the font should be italicised (default is False)
    :param videos: A dictionary of the videos and their names to pre-load to the font cache. Use "path" to specify the path to the file. See the Video page of the docs for the remainder of the options. (there are alot)
    :param models: A dictionary of the 3D Models and their names to pre-load to the 3D model cache. Use "path" to specify the path to the file. See the Video page of the docs for the remainder of the options. (there are alot)
    :param development_screen_size: The size of the screen you develop with. We recomend 800x500. The screen can be scaled to the user's screen with different configurations (see below)
    :param refresh_rate: The maximum refresh rate of the game. Note: all movement is time-based, and independent of the framerate
    :param caption: The text to be shown as the game window's title 
    :param icon: the path to the image to set as the window's icon
    :param loading_screen: The reference to the function to use as the loading animation. The function must take 1 arguement, which is the PyGame surface to do all of the drawing to
    :param min_loading_time: The mimumum amount of loading time the user will see on game launch. The game will load in the background. On completion, if there is still time left, your animation will continue until this time has been met
    :param custom_objects: The list of the refrences of the classes of your custom objects used in the XML. NOTE: Each object MUST inherit from the ObjectBase class (from SideScroller.Objects.ObjectBase import ObjectBase) 
    :param enable_alt_f4: If the window should be closable via the Alt+F4 keyboard shortcut
    :param initial_variables: A dictionary of the variables, and initial values (usefull when objects require variables to load)
    :param fullscreen: If the game should run in fullscreen mode
    :param debug: If the game should run in debug mode (every object is drawn with the hitbox showing)
    :param debug_color: The color to draw the debug hitbox (can be specified individually per Object) 
    :param auto_scale: If the engine should scale the screen to best fit the user's monitor 
    :param default_image: The name of the image (saved in the cache) to be used in the event of an unknown image requested from the cahce
    :param default_spritesheet: The name of the spritesheet (saved in the cache) to be used in the event of an unknown spritesheet requested from the cahce
    :param post_load: The funtion which will be called after everything has been loaded, but before the game starts
    :param alt_side_scroller: An alternate SideScroller class to use as the core engine. NOTE: MUST INHERIT FROM SideScroller CLASS in SideScroller/SideScroller.py
    :param background_color: The color of the screen's background (empty space where nothing is drawn). The default is black (0, 0, 0)
    :param load_mode: The mode ID of the method to interpret the level data as (0=XML, 1=JSON) WARNING: Experamantal
    :param audio_anaylasis_enabled: If the system should allow audio anaylasis. (You need to install 'aubio' first, which many people have issues with)
    """
    tmp = []

    set_sys_var("audio-anaylasis-enabled", audio_anaylasis_enabled)

    if custom_objects is None:
        custom_objects = []

    for sublist in custom_objects:
        if type(sublist) is list:
            for item in sublist:
                tmp.append(item)
        else:
            tmp.append(sublist)
    custom_objects = tmp[:]
    del tmp

    set_sys_var("debug", debug)
    set_sys_var("debug-color", debug_color)

    def termanate():
        if game.room.quit_action():
            quit()

    if initial_variables is None:
        initial_variables = {}

    set_var("vertical_g", -9.80665)
    set_var("lateral_g", 0)

    for name, value in initial_variables.items():
        set_var(name, value)

    if custom_objects is None:
        custom_objects = []

    if development_screen_size is None:
        development_screen_size = get_monitor_resolution()

    game_screen_size = get_monitor_resolution()

    x_scale = game_screen_size[0] / development_screen_size[0]
    y_scale = game_screen_size[1] / development_screen_size[1]

    scale_factor = 1

    if development_screen_size[0] * y_scale <= game_screen_size[0]:
        scale_factor = y_scale
    elif development_screen_size[1] * x_scale <= game_screen_size[1]:
        scale_factor = x_scale
    else:
        quit()

    scaled_size = (
        int(development_screen_size[0] * scale_factor),
        int(development_screen_size[1] * scale_factor)
    )
    scaled_pos = (
        (game_screen_size[0] / 2) - (scaled_size[0] / 2),
        (game_screen_size[1] / 2) - (scaled_size[1] / 2)
    )

    mode = 0
    if fullscreen: mode = pygame.FULLSCREEN

    if auto_scale:
        main_surf = pygame.display.set_mode(game_screen_size, mode | pygame.DOUBLEBUF)
    else:
        main_surf = pygame.display.set_mode(development_screen_size, mode | pygame.DOUBLEBUF)

    screen = pygame.Surface(development_screen_size)

    pygame.display.set_caption(caption)

    if loading_screen is not None:
        t = threading.Thread(
            target=loading_screen,
            args=(screen,)
        )
        t.setDaemon(True)
        t.start()

    load_start = time.time()

    if sprite_sheets is None:
        sprite_sheets = {}

    if images is None:
        images = {}

    if sounds is None:
        sounds = {}

    if font is None:
        font = {}

    if videos is None:
        videos = {}

    if models is None:
        models = {}

    if icon is not None:
        pygame.display.set_icon(pygame.image.load(icon))

    for name, props in images.items():
        set_image(name, props['path'], get_optional(props, "w", None), get_optional(props, "h", None))

    for name, props in sprite_sheets.items():
        set_spritesheet(name, props["path"], props["w"], props["h"], props["duration"], get_optional(props, "final_size", None), get_optional(props, "invisible_color", (10, 10, 10)))

    for name, props in sounds.items():
        set_sound(name, props["path"], get_optional(props, "volume", 1.0, float))

    for name, props in font.items():
        set_font(name, props["path"], props["size"], bold=get_optional(props, "bold", False, bool), italic=get_optional(props, "italic", False, bool))

    for name, props in videos.items():
        set_video(
            name, props["path"],
            has_mask=get_optional(props, "has_mask", False, bool),
            audio=get_optional(props, "audio", True, bool),
            audio_buffersize=get_optional(props, "audio_buffersize", 200000, int),
            target_resolution=get_optional(props, "target_resolution", None, eval),
            resize_algorithm=get_optional(props, "resize_algorithm", 'bicubic', str),
            audio_fps=get_optional(props, "audio_fps", 44100, int),
            audio_nbytes=get_optional(props, "audio_nbytes", 2, int),
            verbose=get_optional(props, "verbose", False, bool),
            fps_source=get_optional(props, "fps_source", 'tbr', str)
        )

    for name, props in models.items():
        set_model(name, path=props["path"])

    set_default_image(default_image)
    set_default_spritesheet(default_spritesheet)

    clock = pygame.time.Clock()
    class_ref = PyGE
    if alt_side_scroller is not None:
        class_ref = alt_side_scroller
    game = class_ref(screen, level_data, start_room, custom_objects, load_mode, background_color)

    load_duration = time.time() - load_start
    if load_duration < min_loading_time:
        time.sleep(min_loading_time - load_duration)

    if post_load is not None:
        post_load()

    set_var("loaded", True)

    i = 1
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                termanate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT or event.mod & pygame.KMOD_RALT) and enable_alt_f4:
                    termanate()

        i += 1

        game.update(events)
        game.draw()

        if auto_scale:
            main_surf.blit(pygame.transform.scale(screen, scaled_size), scaled_pos)
        else:
            main_surf.blit(screen, (0, 0))

        pygame.display.update()

        clock.tick(refresh_rate)
