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

# Initialize session state for volume if it's not already set
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

# Display the current volume
st.success(f"Volume currently set to {st.session_state.volume}%")

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
