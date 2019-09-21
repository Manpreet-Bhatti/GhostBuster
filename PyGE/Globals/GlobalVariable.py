import threading

VARIABLES = {
    "loaded": False,
    "current_pitch": 0.0
}
threads = []

def new_thread(target:callable, name:str, start:bool, *args, **kwargs):
    """
    Spawns and returns a new thread (can not be killed)
    Also adds the thread to the list of system threads used by the engine
    :param target: the function to call for the thread
    :param name: the thread's name
    :param start: if the thread should be started when created
    :param args: other positional arguements to run the function with
    :param kwargs: other named arguements to run the function with
    :return: the newly created thread
    """
    p = threading.Thread(
        target=target,
        name=name,
        args=args,
        kwargs=kwargs
    )
    p.setDaemon(True)
    if start:
        p.start()
    threads.append(p)
    return p

def set_var(key, value):
    """
    Sets a global variable
    :param key: The name of the variable
    :param value: The value of the variable
    """
    VARIABLES[key] = value

def get_var(key):
    """
    Returns a global variable
    :param key: The name of the variable
    :return: The value of the variable
    """
    return VARIABLES[key]

def get_vars():
    """
    Returns all of the saved variables
    :return: A dictionary of each variable
    """
    return VARIABLES

def show_vars():
    """
    Prints all of the variables and values to the console in Name/Value format
    """
    print(VARIABLES)


#
# WARNING:
# SYS VARIABLES ARE PRIVATE
# AND SHOULD NOT BE GIVEN A DOCSTRING!
#

SYS_VARS = {
    "debug": False,
    "debug-color": (255, 255, 255),
    "audio-anaylasis-enabled": False
}

def set_sys_var(key, value):
    SYS_VARS[key] = value

def get_sys_var(key):
    return SYS_VARS[key]

def get_sys_vars():
    return SYS_VARS

def show_sys_vars():
    print(SYS_VARS)
