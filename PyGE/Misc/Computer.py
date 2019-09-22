#from screeninfo import get_monitors #Uncomment if on Windows


def get_monitor_resolution(monitor: int = 0):
    """
    Returns the resolution (size) of the monitor
    :param monitor: The monitor index (0 = primary monitor) This is only needed if the user has specified they want the game to run in a different monitor
    :return: The resolution (size) of the monitor in the format (width, height)
    """
    #selected_monitor = get_monitors()[monitor] #Uncomment if on Windows
    #return selected_monitor.width, selected_monitor.height #Uncomment if on Windows
    return 800, 600 #comment out if on Windows
