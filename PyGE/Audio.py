import pygame

CHANNELS = 8
pygame.mixer.init(channels=CHANNELS)

channels = []

for c in range(CHANNELS):
    channels.append(pygame.mixer.Channel(c))


def get_free_channel():
    """
    This function searches the pool of channels for a free one
    :return: A free channel
    """
    index = -1
    for chan in channels:
        index += 1
        if chan.get_busy() == 0:
            return chan


def playsound(sound):
    """
    Plays a sound on a free channel
    :param sound: Any sound object (We recomend you only use sounds in the cache, however, you can load a new sound and play it here) 
    """
    chan = get_free_channel()
    chan.play(sound)
