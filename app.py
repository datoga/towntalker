# Import from standard library
import logging

# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
from _towntalker import generate_audio, save_audio, get_voices
from _mp3 import musicalize
from _redis import push
    
def generate_mp3_ui(voice, message, out):
    audio = generate_audio(voice=voice, message=message)
    st.session_state.audio = audio
    save_audio(audio=audio, out=out)

    musicalize(messages=[out], music="music.mp3", out="musicalized.mp3", times=2)
    st.session_state.musicalized_file_path = "musicalized.mp3"

def push_message_ui(message, audio_file):
    push(message=message)
    
    with open(audio_file, "rb") as f:
        audio = f.read()
        f.close()
    
    push(message=audio)
    
    st.session_state.message_sent = True


@st.cache_data
def get_voices_ui():
    return get_voices()

logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

st.set_page_config(page_title="TownTalker", page_icon="🎧")

# Store the initial value of widgets in session state
if "name" not in st.session_state:
    st.session_state.name = ""

if "audio" not in st.session_state:
    st.session_state.audio = ""

if "message_sent" not in st.session_state:
    st.session_state.message_sent = False

if "output_file_path" not in st.session_state:
    st.session_state.output_file_path = ""

if "musicalized_file_path" not in st.session_state:
    st.session_state.musicalized_file_path = ""
    
if "text_error" not in st.session_state:
    st.session_state.text_error = ""


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

st.title("TownTalker")

st.markdown(
    "Town message IA generation (message publishing)"
)

def format_func(option):
    name = option.name

    if option.category == 'cloned':
        name += " (custom - " + option.description + ")"

    return name

if st.session_state.message_sent:
    st.toast("Message sent successfully", icon='🎉')
    st.session_state.message_sent = True

voice = st.selectbox('Choose your voice', get_voices_ui(), format_func=format_func)

message = st.text_area(label="Message", placeholder="Write here the message", height=100)

# Create a button to generate the message.
if st.button(
    label="Generate message",  # name on the button
    help="Click to generate the message",  # hint text (on hover)
    key="generate_message",  # key to be used for the button
    type="primary",  # red default streamlit button
    on_click=generate_mp3_ui,  # function to be called on click
    args=(voice, message, "out.mp3"),  # arguments to be passed to the function
):
    st.write('This is your raw message')
    st.audio(st.session_state.audio)
    st.write('And this is your complete message')
    st.audio(st.session_state.musicalized_file_path)

    st.button(
        label="Send message",  # name on the button
        help="Click to send the message",  # hint text (on hover)
        key="send_message",  # key to be used for the button
        type="primary",  # red default streamlit button
        on_click=push_message_ui,  # function to be called on click
        args=(message, st.session_state.musicalized_file_path),  # arguments to be passed to the function
    )
