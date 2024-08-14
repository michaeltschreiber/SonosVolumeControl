import soco
from soco import SoCo
import streamlit as st

# Discover all Sonos speakers in the network
speakers = list(soco.discover())

# Filter to find the Living Room speaker
living_room_speaker = next((speaker for speaker in speakers if speaker.player_name == "Living Room"), None)

if living_room_speaker is None:
    st.error("Living Room speaker not found. Please ensure it is online and try again.")
else:
    st.title("Sonos Living Room Controller")

    # Create two columns for buttons
    col1, col2 = st.columns(2)

    # Create buttons in two columns for each volume level (0% - 100% in 10% steps)
    buttons = [col1.button if i < 60 else col2.button for i in range(0, 101, 10)]

    for i, button in zip(range(0, 101, 10), buttons):
        if button(f"Set volume to {i}%"):
            # Set the volume
            living_room_speaker.volume = i
            st.success(f"Volume set to {i}%")

# Note: You should run this script on a network that includes your Sonos speakers.
