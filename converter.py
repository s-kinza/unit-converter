import streamlit as st
from pint import UnitRegistry
import speech_recognition as sr

import pyttsx3




# Create an instance of UnitRegistry
ureg = UnitRegistry()

st.title("🏪 Unit Converter")

# Create dictionary of units 
# Define Units Catogory

categories = {

    "Length" : ["meters", "kilometers", "mile", "foot", "inch"],
    "Weight" : ["kilograms", "grams", "pounds", "ounces"],
    "Temperature" : ["celsius", "fahrenheit", "kelvin"],
    "Speed" : ["m/s", "km/h", "mph"],

}

# User Selection
st.subheader("Select Conversion Type:")
category = st.selectbox("Choose a category", list(categories.keys()))
from_unit = st.selectbox("From Unit", categories[category])
to_unit = st.selectbox("To Unit", categories[category])
value = st.number_input("Enter Value", min_value=0.0)

# Conversion Logic
if st.button("Convert"):
    try:
        if category == "Temperature":
            # Manual Temperature Conversion
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            else:
                result = value  # Same unit case
        else:
            result = (value * ureg(from_unit)).to(to_unit)

        st.success(f"{value} {from_unit} = {result} {to_unit}")
    
    except Exception as e:
        st.error(f"Conversion Error: {e}")


# Speech Recognition

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak Now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)  # Google Speech Recognition API
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("😕 Sorry, could not understand the audio.")
    except sr.RequestError:
        st.error("❌ Could not request results, check internet connection.")
    return None

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if st.button("🎙️ Speak & Convert"):
    spoken_text = voice_input()  # User ki awaz ko text me convert karein
    if spoken_text:
        value = float(spoken_text)  # Speech-to-Text se number extract karein
        if category and from_unit and to_unit:
            # Conversion Logic
            if category == "Temperature":
                if from_unit == "celsius" and to_unit == "fahrenheit":
                    result = (value * 9/5) + 32
                elif from_unit == "fahrenheit" and to_unit == "celsius":
                    result = (value - 32) * 5/9
                elif from_unit == "celsius" and to_unit == "kelvin":
                    result = value + 273.15
                elif from_unit == "kelvin" and to_unit == "celsius":
                    result = value - 273.15
                else:
                    result = value  # Same unit case
            else:
                result = ureg.Quantity(value, from_unit).to(to_unit)

            st.success(f"{value} {from_unit} = {result} {to_unit}")

            # 🗣️ Speak the Result
            text_to_speech(f"{value} {from_unit} equals {result} {to_unit}")


st.sidebar.title("About")
st.sidebar.subheader("Unit Converter App")
st.sidebar.text("This app allows you to convert units of measurement for various categories such as Length, Weight, Temperature, and Speed.")

# Add a multiselect
selected_units = st.sidebar.multiselect("Select units you frequently use:", ["meters", "kilograms", "celsius", "m/s", "kilometers", "grams", "pounds", "ounces", "fahrenheit", "kelvin", "mile", "foot", "inch", "km/h", "mph"])

# Add a checkbox
show_advanced_options = st.sidebar.checkbox("Show advanced options")

# Add radio buttons
conversion_mode = st.sidebar.radio("Conversion Mode:", ["Standard", "Scientific"])

# Add a date input
conversion_date = st.sidebar.date_input("Select conversion date:")

# Add a button
if st.sidebar.button("Submit"):
    st.sidebar.write(f"Selected units: {selected_units}")
    st.sidebar.write(f"Advanced options: {'Enabled' if show_advanced_options else 'Disabled'}")
    st.sidebar.write(f"Conversion mode: {conversion_mode}")
    st.sidebar.write(f"Conversion date: {conversion_date}")

