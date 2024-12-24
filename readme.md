# Atmosphere Sync Tool 🌤️

**Atmosphere Sync Tool** is a Streamlit-based weather application that provides accurate, real-time weather updates by consolidating data from multiple weather APIs. It visually represents weather conditions with dynamic elements, making weather information intuitive and engaging.

---

## 🌟 Features
- **Accurate Weather Data:** Aggregates and reconciles weather data from OpenWeatherMap, WeatherAPI, and AccuWeather for improved reliability.
- **Interactive UI:** User-friendly interface built with Streamlit for a seamless experience.
- **Dynamic Visuals:** Displays a facial expression and color-coded mood representation based on current weather conditions.
- **Comprehensive Weather Metrics:** Shows temperature, humidity, wind speed, and condition.
- **Global Coverage:** Enter any city name to get weather data for locations around the world.

---

## 📋 Requirements
Ensure you have the following installed:
- Python 3.8 or higher
- Required libraries in `requirements.txt` (see below)

---

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/gautamraj8044/atmosphere-sync-tool.git
   cd atmosphere-sync-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your API keys:
     ```env
     OPENWEATHERMAP_API = "your_openweathermap_api_key"
     WEATHERAPI_API = "your_weatherapi_api_key"
     ACCUWEATHER_API = "your_accuweather_api_key"
     ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Project Structure
```
.
├── app.py                # Main Streamlit app
├── utils/
│   ├── weather_fetcher.py # Fetches weather data from APIs
│   ├── weather_reconciler.py # Harmonizes weather data
├── resources/
│   ├── styles.css         # Custom CSS styles
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (API keys)
├── README.md              # Project documentation
```

---

## 🌐 APIs Used
- [OpenWeatherMap](https://openweathermap.org/)
- [WeatherAPI](https://www.weatherapi.com/)
- [AccuWeather](https://developer.accuweather.com/)

---

## 📊 How It Works
1. **User Input:** Enter a city name in the text box.
2. **Fetch Weather Data:** Retrieves weather information from three different APIs.
3. **Reconcile Data:** Harmonizes the fetched data for consistency and reliability.
4. **Display Metrics:** Shows key weather parameters and visualizes the "weather mood" through a dynamic face.

---

## 🎨 Visual Representation
- **Face Color:**
  - Blue: Cold weather (temperature < 10°C)
  - Yellow: Moderate weather (10°C ≤ temperature ≤ 25°C)
  - Red: Hot weather (temperature > 25°C)
- **Facial Expressions:**
  - Smile: Clear or sunny conditions
  - Neutral: Mixed conditions
  - Frown: Rain, storm, or adverse conditions
- **Eyes:** Adjusts based on wind speed (narrow, normal, or wide).

---

## 🚀 Future Enhancements
- Add support for more weather APIs.
- Include a historical weather data chart.
- Integrate user location auto-detection.
- Enable forecast visualization for upcoming days.

---

## 🤝 Contributing
Contributions are welcome! If you'd like to improve this project, follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.



## 📧 Contact
For any queries or feedback, feel free to contact:
- **Name:** Gautam Raj  
- **Email:** gautamraj8044@gmail.com  
- **GitHub:** [gautamraj8044](https://github.com/gautamraj8044)

Enjoy exploring the weather with **Atmosphere Sync Tool**! 🌍
