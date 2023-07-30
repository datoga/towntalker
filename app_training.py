# Import from standard library
import os
import logging

# Import from 3rd party libraries
import streamlit as st
from audio_recorder_streamlit import audio_recorder

# Import modules from the local package
from _towntalker import clone_voice, generate_audio, get_voices

def get_voices_ui():
    return get_voices()

logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

st.set_page_config(page_title="TownTalker", page_icon="🎧")

# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("TownTalker (cloning)")

st.markdown(
    "Town message IA generation - cloning"
)

name = st.text_input(label="Name", placeholder="Name of the voice")

if any(voice.name == name for voice in get_voices_ui()):
    st.error('This voice name is being used, try another one')

audio_bytes = audio_recorder(
    text="Click to record, please read a 30 seconds message with your voice, in a quiet place. You will get better results if you use a microphone.",
    energy_threshold=(-1.0, 1.0),
    pause_threshold=30.0,
)

if audio_bytes:
    st.audio(audio_bytes)
    filename = "sample.mp3"

    with open(filename, "wb") as f:
        f.write(audio_bytes)
    
    voice = clone_voice(name=name, training_file_path=filename)

    message = "This is a test message generated with your cloned voice, you can either keep it or try to clone it again"
    audio = generate_audio(voice=voice, message=message)
    st.write(message)
    st.audio(audio)

file = st.file_uploader(label="Upload music", type=["mp3",])
if file is not None:
    filename = "music.mp3"
    with open(filename, "wb") as f:
        f.write(file.getbuffer())


