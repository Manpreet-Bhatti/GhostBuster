from PyGE.Globals.GlobalVariable import set_var, get_sys_var

import numpy as num


def frequency_monitor(unit="Hz", silence=-40):
    """
    WARNING: Temporarily Disabled!
    Monitors the frequency (pitch) of the audio input.
    WARNING: DO NOT CALL IN MAIN THREAD!!!
    :param unit: the unit to measure the pitch in (default is "Hz" - Hertz)
    :param silence: The silence threashold (default is -40db)
    """
    if not get_sys_var("audio-anaylasis-enabled"):
        raise ValueError("Please Enable Audio Anaylasis In The Main Function Call (Set Paramater audio_anaylasis_enabled To True)")
    import aubio
    import pyaudio

    # constants
    buffer_size = 2048
    channels = 1
    pyaudio_format = pyaudio.paFloat32
    method = "default"
    sample_rate = 44100
    hop_size = buffer_size // 2
    period_size_in_frame = hop_size

    # Initiating PyAudio object.
    pa = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pa.open(
        format=pyaudio_format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=period_size_in_frame
    )

    # Initiating Aubio's pitch detection object.
    detection = aubio.pitch(method, buffer_size,
        hop_size, sample_rate)
    # Set unit.
    detection.set_unit(unit)
    # Frequency under -40 dB will considered
    # as a silence.
    detection.set_silence(silence)

    while True:
        # Always listening to the microphone.
        data = mic.read(period_size_in_frame)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data, dtype=aubio.float_type)
        # Finally get the pitch.
        set_var("current_pitch", detection(samples)[0])
