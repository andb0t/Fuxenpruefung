import winsound

import files

SOUND_IS_ON = False


def sound():
    return SOUND_IS_ON


def sound_button_image():
    return files.resource_path('', 'images\\' + toggle_sound(False) + '.png')


def start_sound():
    global SOUND_IS_ON
    songWav = files.resource_path('', r'sounds\Ehr_unser_Zier.wav')
    winsound.PlaySound(songWav, winsound.SND_FILENAME | winsound.SND_ASYNC)
    SOUND_IS_ON = True


def stop_sound():
    global SOUND_IS_ON
    winsound.PlaySound(None, winsound.SND_PURGE)
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
