import winsound

import files

SOUND_IS_ON = False


def start_sound():
    global SOUND_IS_ON
    songWav = files.resource_path('', r'sounds\Ehr_unser_Zier.wav')
    winsound.PlaySound(songWav, winsound.SND_FILENAME | winsound.SND_ASYNC)
    SOUND_IS_ON = True


def stop_sound():
    global SOUND_IS_ON
    winsound.PlaySound(None, winsound.SND_PURGE)
    SOUND_IS_ON = False


def toggle_sound():
    if SOUND_IS_ON:
        stop_sound()
        return 'mute'
    else:
        start_sound()
        return 'sound'
