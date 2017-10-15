import winsound

import files

SOUND_IS_ON = False


def sound():
    return SOUND_IS_ON


def sound_button_image():
    return files.resource_path('', 'images\\' + toggle_sound(False) + '.png')


def start_sound():
    global SOUND_IS_ON
    winsound.PlaySound(files.SONG_WAV_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
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


def play_sound(sound):
    winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)


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
