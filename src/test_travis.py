import pyaudio
import requests


print('Hello travis world!')

pa = pyaudio.PyAudio()

print('Survived it! Now play sound...')

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


print('open stream using callback')

stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(),
                 rate=wf.getframerate(),
                 output=True,
                 stream_callback=callback)

stream.stop_stream()

print('Survived it!')
