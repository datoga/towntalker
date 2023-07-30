from pydub import AudioSegment

def musicalize(messages, music, out='out.mp3', times=1, gap=3):
    music_sound = AudioSegment.from_mp3(music)
    silence = AudioSegment.silent(duration=gap*1000)

    payload = AudioSegment.silent(duration=1)

    for message in messages:
        message_sound = AudioSegment.from_mp3(message)
        payload = payload + message_sound + silence

    payload = payload * times

    complete = music_sound + silence + payload + music_sound

    complete.export(out, format="mp3")

    return
 
