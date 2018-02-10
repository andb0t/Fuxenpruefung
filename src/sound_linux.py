import pyaudio
import wave

import files


SOUND_IS_ON = False

wf = wave.open(files.SONG_WAV_PATH, 'rb')

# instantiate PyAudio (1)
pa = pyaudio.PyAudio()


# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


# open stream using callback (3)
stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(),
                 rate=wf.getframerate(),
                 output=True,
                 stream_callback=callback)

stream.stop_stream()


def sound():
    return SOUND_IS_ON


def sound_button_image():
    return files.resource_path('', 'images\\' + toggle_sound(False) + '.png')


def start_sound():
    global SOUND_IS_ON

    # start the stream (4)
    stream.start_stream()

    SOUND_IS_ON = True


def stop_sound():
    global SOUND_IS_ON

    # stop stream (6)
    stream.stop_stream()
    # stream.close()
    # wf.close()
    # close PyAudio (7)
    # p.terminate()

    SOUND_IS_ON = False


def toggle_sound(doSwitch=True):
    if sound():
        if doSwitch:
            stop_sound()
        return 'sound'
    else:
        if doSwitch:
            start_sound()
        return 'mute'


def play_sound(sound):
    try:
        wf = wave.open(sound, 'rb')

        # instantiate PyAudio (1)
        pa = pyaudio.PyAudio()

        # define callback (2)
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # open stream using callback (3)
        stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output=True,
                         stream_callback=callback)

        # start the stream (4)
        stream.start_stream()
    except wave.Error:
        print('Warning: caught wave.Error!')


def main():
    print('Playing the sound on your system!')
    start_sound()
    print('Hit <enter> key to toggle sound on and off!')
    while True:
        pressedKey = input()
        if pressedKey == '':
            toggle_sound()


if __name__ == '__main__':
    main()
