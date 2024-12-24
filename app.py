import streamlit as st
from typing import Dict
import streamlit.components.v1 as components
from utils.weather_fetcher import WeatherFetcher

class WeatherMood:
    def __init__(self, weather_data: Dict):
        self.weather_data = weather_data
        self.setup_styles()

    def setup_styles(self):
        with open('resources/styles.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def draw_face(self):
        if not self.weather_data.get("temperature"):
            st.error("Unable to retrieve weather data")
            return

        if self.weather_data.get("city") and self.weather_data.get("country"):
            st.markdown(
                f"<h2 class='location-text'>{self.weather_data['city']}, {self.weather_data['country']}</h2>",
                unsafe_allow_html=True
            )

        face_container = st.container()
        with face_container:
            eye_state = self._calculate_eye_state()
            face_color = self._calculate_face_color()
            expression = self._calculate_expression()
            components.html(
                self._generate_face_html(eye_state, face_color, expression),
                height=100
            )

        st.markdown("### Current Weather")
        weather_container = st.container()
        with weather_container:
            left_col, right_col = st.columns(2)
            
            with left_col:
                st.metric("Temperature", f"{self.weather_data['temperature']}°C")
                st.metric("Wind Speed", f"{self.weather_data['wind_speed']} m/s")
            
            with right_col:
                st.metric("Humidity", f"{self.weather_data['humidity']}%")
                st.metric("Condition", self.weather_data.get('condition', 'Unknown').title())

    def _calculate_eye_state(self):
        wind_speed = self.weather_data.get('wind_speed', 0)
        return 'narrow' if wind_speed > 15 else 'normal' if wind_speed > 5 else 'wide'

    def _calculate_face_color(self):
        temp = self.weather_data.get('temperature', 20)
        if temp < 10: return '#0074D9'
        elif temp > 25: return '#FF4136'
        return '#FFDC00'

    def _calculate_expression(self):
        condition = self.weather_data.get('condition', '').lower()
        if any(w in condition for w in ['rain', 'storm', 'snow', 'mist', 'drizzle']):
            return 'frown'
        elif any(w in condition for w in ['clear', 'sunny']):
            return 'smile'
        return 'neutral'

    def _generate_face_html(self, eye_state, face_color, expression):
        return f"""
            <div class="weather-face" style="background-color:{face_color};">
                <div class="eyes">
                    <div class="eye" style="opacity:{0.5 if eye_state == 'narrow' else 1};"></div>
                    <div class="eye" style="opacity:{0.5 if eye_state == 'narrow' else 1};"></div>
                </div>
                <div class="mouth" style="transform: {'' if expression == 'smile' else 'rotate(180deg)'}"></div>
            </div>
        """

def main():
    st.set_page_config(
        page_title="Atmosphere Sync Tool",
        page_icon="🌤️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown(
        "<h1 style='text-align: center;'>☁️ Atmosphere Sync Tool</h1>",
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        location = st.text_input(
            "Enter city name:",
            "London",
            help="Enter a city name to see its current weather mood"
        )
    
        if st.button("Get Weather", use_container_width=True):
            with st.spinner("Fetching weather data..."):
                fetcher = WeatherFetcher()
                weather_data = fetcher.get_weather(location)
                
                if weather_data.get("temperature") is not None:
                    mood = WeatherMood(weather_data)
                    mood.draw_face()
                else:
                    st.error("Could not find weather data for this location. Please check the city name and try again.")

if __name__ == "__main__":
    main()