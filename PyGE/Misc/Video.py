from moviepy.editor import *            # pip3 install moviepy
import pygame



class Video:
    def __init__(
            self, path, has_mask=False, audio=True, audio_buffersize=200000, target_resolution=None,
            resize_algorithm='bicubic', audio_fps=44100, audio_nbytes=2, verbose=False, fps_source='tbr'
    ):
        """
        A video object
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

        self.fps_source = fps_source
        self.verbose = verbose
        self.audio_nbytes = audio_nbytes
        self.audio_fps = audio_fps
        self.resize_algorithm = resize_algorithm
        self.target_resolution = target_resolution
        self.audio_buffersize = audio_buffersize
        self.audio = audio
        self.has_mask = has_mask

        if self.target_resolution is None:
            self.target_resolution = pygame.display.get_surface().get_size()

        self.video = VideoFileClip(
            path, has_mask, audio
        )

    def play(self):
        """
        Plays the video
        """
        self.video.preview()