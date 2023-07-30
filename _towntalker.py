from elevenlabs import set_api_key, generate, voices, clone, save, VOICES_CACHE
import time
import os


# Here we are setting up the ElevenLabs API key.
set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

def clone_voice(name, training_file_path):
    voice = clone(
        name=name,
        description="The perfect voice to read news in a town",
        files=[training_file_path,],
    )

    return voice

def generate_audio(voice, message):
    audio = generate(
      text=message,
      voice=voice,
      model="eleven_multilingual_v1"
    )
   
    return audio
   
def save_audio(audio, out):
    save(audio=audio, filename=out)

def get_voices():
    cloned = []
    builtin = []

    v_list = voices()

    for v in v_list:
        if v.category == 'cloned':
          cloned.append(v)
        else:
          builtin.append(v)

    names = cloned + builtin

    return names