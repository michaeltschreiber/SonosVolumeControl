import soco
from soco import SoCo
import streamlit as st

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Discover all Sonos speakers in the network
speakers = list(soco.discover())

# Filter to find the Living Room speaker
living_room_speaker = next((speaker for speaker in speakers if speaker.player_name == "Living Room"), None)

if living_room_speaker is None:
    st.error("Living Room speaker not found. Please ensure it is online and try again.")
else:
    st.title("Sonos Living Room Controller")


# Get the current volume of the speaker if the user has not set it via query parameters; otherwise, set the volume
if 'volume' not in st.session_state:
    if 'volume' in st.query_params:
        try:
            query_volume = int(st.query_params['volume'])
            if 0 <= query_volume <= 100:
                st.session_state.volume = query_volume
                living_room_speaker.volume = query_volume
        except ValueError:
            st.error("Invalid volume parameter. Please use an integer between 0 and 100.")
    else:
        st.session_state.volume = living_room_speaker.volume

# Get the "night_mode" status of the speaker if the user has not set it via query parameters; otherwise, set the "night_mode" status
if 'night_mode' not in st.session_state:
    if 'night_mode' in st.query_params:
        try:
            query_night_mode = st.query_params['night_mode'].lower()
            if query_night_mode == "true":
                st.session_state.night_mode = True
                living_room_speaker.night_mode = True
            elif query_night_mode == "false":
                st.session_state.night_mode = False
                living_room_speaker.night_mode = False
            else:
                st.error("Invalid night_mode parameter. Please use 'true' or 'false'.")
        except ValueError:
            st.error("Invalid night_mode parameter. Please use 'true' or 'false'.")
    else:
        st.session_state.night_mode = living_room_speaker.night_mode

# Get the "dialog_mode" status of the speaker if the user has not set it via query parameters; otherwise, set the "dialog_mode" status
if 'dialog_mode' not in st.session_state:
    if 'dialog_mode' in st.query_params:
        try:
            query_dialog_mode = st.query_params['dialog_mode'].lower()
            if query_dialog_mode == "true":
                st.session_state.dialog_mode = True
                living_room_speaker.dialog_mode = True
            elif query_dialog_mode == "false":
                st.session_state.dialog_mode = False
                living_room_speaker.dialog_mode = False
            else:
                st.error("Invalid dialog_mode parameter. Please use 'true' or 'false'.")
        except ValueError:
            st.error("Invalid dialog_mode parameter. Please use 'true' or 'false'.")
    else:
        st.session_state.dialog_mode = living_room_speaker.dialog_mode

# Get the "sub_enabled" status of the speaker if the user has not set it via query parameters; otherwise, set the "sub_enabled" status
if 'sub_enabled' not in st.session_state:
    if 'sub_enabled' in st.query_params:
        try:
            query_sub_enabled = st.query_params['sub_enabled'].lower()
            if query_sub_enabled == "true":
                st.session_state.sub_enabled = True
                living_room_speaker.sub_enabled = True
            elif query_sub_enabled == "false":
                st.session_state.sub_enabled = False
                living_room_speaker.sub_enabled = False
            else:
                st.error("Invalid sub_enabled parameter. Please use 'true' or 'false'.")
        except ValueError:
            st.error("Invalid sub_enabled parameter. Please use 'true' or 'false'.")
    else:
        st.session_state.sub_enabled = living_room_speaker.sub_enabled

# Get the 'sub_gain' status of the speaker if the user has not set it via query parameters; otherwise, set the 'sub_gain' (int ranging from -15 to 15)
if 'sub_gain' not in st.session_state:
    if 'sub_gain' in st.query_params:
        try:
            query_sub_gain = int(st.query_params['sub_gain'])
            if -15 <= query_sub_gain <= 15:
                st.session_state.sub_gain = query_sub_gain
                living_room_speaker.sub_gain = query_sub_gain
        except ValueError:
            st.error("Invalid sub_gain parameter. Please use an integer between -15 and 15.")
    else:
        st.session_state.sub_gain = living_room_speaker.sub_gain

# st.success(f"Volume currently set to {st.session_state.volume}")

# Slider for volume control
new_volume = st.slider("Set volume", min_value=0, max_value=100, value=st.session_state.volume, step=5)
# Update the volume if the slider is changed
if new_volume != st.session_state.volume:
    living_room_speaker.volume = new_volume
    st.session_state.volume = new_volume
    st.query_params['volume']=new_volume
    st.rerun()

# Create two columns for buttons
col1, col2 = st.columns(2)

# Create buttons in two columns for each volume level (0% - 100% in 10% steps)
buttons = [col1.button if i < 60 else col2.button for i in range(0, 101, 10)]

for i, button in zip(range(0, 101, 10), buttons):
    if button(f"Set volume to {i}%"):
        # Set the volume
        living_room_speaker.volume = i
        st.session_state.volume = i
        st.query_params['volume']=i 
        st.rerun()

#st.success(f"Night mode is {'enabled' if st.session_state.night_mode else 'disabled'}; dialog mode is {'enabled' if st.session_state.dialog_mode else 'disabled'}; subwoofer is {'on' if st.session_state.sub_enabled else 'off'} and sub gain is {st.session_state.sub_gain}.")

# Slider for sub_gain control
new_sub_gain = st.slider("Set sub gain", min_value=-15, max_value=15, value=st.session_state.sub_gain, step=1)
# Update the sub_gain if the slider is changed
if new_sub_gain != st.session_state.sub_gain:
    living_room_speaker.sub_gain = new_sub_gain
    st.session_state.sub_gain = new_sub_gain
    st.query_params['sub_gain']=new_sub_gain
    st.rerun()

# three-column layout for night_mode toggle and dialog_mode toggles
toplcol, topmcol, toprcol = st.columns(3)

# Toggle for night_mode
night_mode = toplcol.checkbox("Night Mode", value=st.session_state.night_mode)
# Update the night_mode status if the checkbox is changed
if night_mode != st.session_state.night_mode:
    living_room_speaker.night_mode = night_mode
    st.session_state.night_mode = night_mode
    st.query_params['night_mode']=str(night_mode).lower()
    st.rerun()

# Toggle for sub_enabled
sub_enabled = topmcol.checkbox("Sub Enabled", value=st.session_state.sub_enabled)
# Update the sub_enabled status if the checkbox is changed
if sub_enabled != st.session_state.sub_enabled:
    living_room_speaker.sub_enabled = sub_enabled
    st.session_state.sub_enabled = sub_enabled
    st.query_params['sub_enabled']=str(sub_enabled).lower()
    st.rerun()

# Toggle for dialog_mode
dialog_mode = toprcol.checkbox("Dialog Mode", value=st.session_state.dialog_mode)
# Update the dialog_mode status if the checkbox is changed
if dialog_mode != st.session_state.dialog_mode:
    living_room_speaker.dialog_mode = dialog_mode
    st.session_state.dialog_mode = dialog_mode
    st.query_params['dialog_mode']=str(dialog_mode).lower()
    st.rerun()