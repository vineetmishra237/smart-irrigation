# 🌱 Smart Irrigation System - AI-Powered Water Management

An advanced AI-powered irrigation system that uses machine learning, real-time weather data, and IoT sensors to optimize water usage for agricultural applications. The system features a modern web dashboard with real-time analytics and predictive irrigation scheduling.

![Smart Irrigation Dashboard](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-red) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

- **🤖 AI-Powered Predictions**: Machine learning model for optimal water discharge calculations
- **🌤️ Real-time Weather Integration**: OpenWeatherMap API for live weather conditions
- **🔥 Firebase Integration**: Real-time soil moisture monitoring from IoT sensors
- **📊 Advanced Analytics**: Water conservation tracking and efficiency metrics
- **💧 Smart Water Management**: Automated irrigation scheduling based on multiple factors
- **📱 Modern Web Interface**: Professional dashboard with real-time data visualization
- **⚡ IoT Compatible**: Direct integration with microcontrollers and sensors
- **🎯 Predictive Intelligence**: ML algorithms for irrigation optimization

## 🖥️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Dashboard │◄──►│   Flask Backend  │◄──►│  Firebase DB    │
│   (Frontend)    │    │   (AI Engine)    │    │  (IoT Sensors)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ OpenWeatherMap   │
                    │     API          │
                    └──────────────────┘
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://python.org/downloads/))
- **Git** ([Download Git](https://git-scm.com/downloads))
- **Code Editor** (VS Code, PyCharm, or any preferred editor)
- **Web Browser** (Chrome, Firefox, Safari, or Edge)

## 🛠️ Installation Guide

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-irrigation-system.git

# Navigate to the project directory
cd smart-irrigation-system
```

### Step 2: Set Up Python Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv smart_irrigation_env

# Activate the virtual environment
# On Windows:
smart_irrigation_env\Scripts\activate

# On macOS/Linux:
source smart_irrigation_env/bin/activate
```

### Step 3: Install Required Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Required packages include:**
- Flask (Web framework)
- numpy (Numerical computing)
- scikit-learn (Machine learning)
- requests (HTTP requests)
- firebase-admin (Firebase integration)

### Step 4: Configure Firebase (Required for IoT Integration)

1. **Create a Firebase Project:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Create a project"
   - Follow the setup wizard

2. **Enable Realtime Database:**
   - In your Firebase project, go to "Realtime Database"
   - Click "Create Database"
   - Choose "Start in test mode" for development

3. **Download Service Account Key:**
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Save the downloaded JSON file as `serviceAccountKey.json` in the project root

4. **Update Database URL:**
   - Open `app.py`
   - Replace the `databaseURL` with your Firebase project URL:
   ```python
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com'
   })
   ```

### Step 5: Configure Weather API (Required for Weather Data)

1. **Get OpenWeatherMap API Key:**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Update API Key in Code:**
   - Open `app.py`
   - Replace the API key in the `get_weather_forecast` function:
   ```python
   api_key = "YOUR_OPENWEATHERMAP_API_KEY"
   ```

## 🚀 Running the Application

### Method 1: Standard Flask Run

```bash
# Make sure you're in the project directory
cd smart-irrigation-system

# Run the Flask application
python app.py
```

### Method 2: Flask Development Server

```bash
# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run with Flask command
flask run --port=5001
```

### Step 6: Access the Dashboard

1. **Open your web browser**
2. **Navigate to:** `http://127.0.0.1:5001` or `http://localhost:5001`
3. **You should see the Smart Irrigation Dashboard**

## 📁 Project Structure

```
smart-irrigation-system/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── serviceAccountKey.json      # Firebase service account (you create this)
├── README.md                   # This file
│
├── templates/
│   └── index.html             # Main dashboard interface
│
└── static/ (optional)
    ├── css/
    ├── js/
    └── images/
```

## 🔧 Configuration Options

### Firebase Database Structure

Your Firebase Realtime Database should have this structure:

```json
{
  "sensor": {
    "humidity": 45.2,
    "temperature": 24.5,
    "timestamp": "2025-09-01T10:30:00Z"
  },
  "control": {
    "pump_runtime_seconds": 120.5,
    "irrigation_status": "idle"
  }
}
```

### Environment Variables (Optional)

Create a `.env` file for sensitive configuration:

```env
OPENWEATHER_API_KEY=your_api_key_here
FIREBASE_DATABASE_URL=https://your-project-default-rtdb.firebaseio.com
FLASK_SECRET_KEY=your_secret_key_here
```

## 🎮 Using the System

### 1. Dashboard Overview

The dashboard provides real-time monitoring of:
- **Weather Conditions**: Temperature, humidity, rainfall
- **Soil Moisture**: Live readings from IoT sensors
- **AI Confidence**: System prediction accuracy
- **Water Efficiency**: Conservation metrics

### 2. Making Irrigation Predictions

1. **Set Parameters:**
   - Valve diameter (inches)
   - Soil type (Sandy/Loamy/Clay)
   - Field coverage area (m²)

2. **Click "Calculate Optimal Irrigation"**

3. **Review Results:**
   - Pump runtime recommendation
   - Water volume calculations
   - Efficiency metrics
   - Cost savings analysis

### 3. Monitoring Analytics

- **Water Conservation**: Track total water saved
- **Efficiency Trends**: Monitor system performance
- **Usage Comparison**: Smart vs traditional irrigation

## 🔌 IoT Integration

### Connecting Sensors

To connect IoT sensors (Arduino, Raspberry Pi, ESP32):

1. **Read from Firebase:**
```python
# Example: Read pump runtime
import firebase_admin
from firebase_admin import db

ref = db.reference('/control/pump_runtime_seconds')
runtime = ref.get()
print(f"Run pump for: {runtime} seconds")
```

2. **Write Sensor Data:**
```python
# Example: Upload soil moisture
ref = db.reference('/sensor')
ref.update({
    'humidity': 42.5,
    'temperature': 23.8,
    'timestamp': datetime.now().isoformat()
})
```

### Example Arduino Integration

```cpp
// Arduino code snippet for ESP32
#include <WiFi.h>
#include <FirebaseESP32.h>

void setup() {
  // Connect to WiFi and Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop() {
  // Read soil moisture sensor
  int moistureValue = analogRead(A0);
  float moisturePercent = map(moistureValue, 0, 1023, 0, 100);
  
  // Upload to Firebase
  Firebase.setFloat(firebaseData, "/sensor/humidity", moisturePercent);
  
  delay(30000); // Update every 30 seconds
}
```

## 🧪 Testing the System

### 1. Test Weather API

```bash
# Test weather endpoint
curl http://localhost:5001/api/weather
```

### 2. Test Soil Moisture API

```bash
# Test soil moisture endpoint
curl http://localhost:5001/api/soil-moisture
```

### 3. Test Prediction

1. Open the dashboard
2. Fill in the form with test values
3. Submit and verify the AI prediction works

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **Module Not Found Errors**
```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

#### 2. **Firebase Connection Issues**
- Verify `serviceAccountKey.json` is in the root directory
- Check that the database URL is correct
- Ensure Firebase Realtime Database is enabled

#### 3. **Weather API Not Working**
- Verify your OpenWeatherMap API key is valid
- Check internet connection
- Ensure API key is properly inserted in `app.py`

#### 4. **Port Already in Use**
```bash
# Solution: Use a different port
python app.py --port=5002
```

#### 5. **Permission Errors**
```bash
# Solution: Run with appropriate permissions
sudo python app.py  # Linux/macOS
# Or run as administrator on Windows
```

## 📊 API Documentation

### Weather API
- **Endpoint**: `/api/weather`
- **Method**: GET
- **Response**: Current weather conditions

### Soil Moisture API
- **Endpoint**: `/api/soil-moisture`
- **Method**: GET
- **Response**: Current soil moisture levels

### Prediction API
- **Endpoint**: `/predict`
- **Method**: POST
- **Parameters**: valve_diameter, soil_type, field_area

### Analytics API
- **Endpoint**: `/stats`
- **Method**: GET
- **Response**: Water usage statistics and charts

## 🔒 Security Considerations

### For Production Deployment

1. **Environment Variables**: Store sensitive data in environment variables
2. **HTTPS**: Use SSL certificates for secure connections
3. **Firebase Rules**: Configure proper database security rules
4. **API Rate Limiting**: Implement rate limiting for APIs
5. **Input Validation**: Add comprehensive input validation

### Firebase Security Rules

```json
{
  "rules": {
    "sensor": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "control": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

## 📈 Performance Optimization

### Tips for Better Performance

1. **Caching**: Implement Redis for API response caching
2. **Database Indexing**: Optimize Firebase queries
3. **Async Processing**: Use Celery for background tasks
4. **CDN**: Use CDN for static assets

## 🚀 Deployment Options

### Option 1: Heroku Deployment

1. **Create `Procfile`:**
```
web: python app.py
```

2. **Deploy:**
```bash
git add .
git commit -m "Deploy to Heroku"
heroku create your-app-name
git push heroku main
```

### Option 2: Docker Deployment

1. **Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
```

2. **Build and Run:**
```bash
docker build -t smart-irrigation .
docker run -p 5001:5001 smart-irrigation
```

### Option 3: Local Server

```bash
# Install gunicorn for production
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Write unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Firebase for real-time database services
- scikit-learn for machine learning capabilities
- Flask community for the web framework
- Tailwind CSS for styling framework

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section above**
2. **Search existing issues**: [GitHub Issues](https://github.com/yourusername/smart-irrigation-system/issues)
3. **Create a new issue**: Include error messages and system information
4. **Contact**: your.email@example.com

## 🔮 Future Enhancements

- [ ] Mobile app development
- [ ] Advanced ML models (LSTM, Neural Networks)
- [ ] Weather forecasting integration
- [ ] Multi-zone irrigation control
- [ ] Crop-specific irrigation algorithms
- [ ] Water quality monitoring
- [ ] Automated scheduling system
- [ ] SMS/Email notifications
- [ ] Historical data analysis
- [ ] Integration with more IoT platforms

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/smart-irrigation-system&type=Date)](https://star-history.com/#yourusername/smart-irrigation-system&Date)

---

**Made with ❤️ for sustainable agriculture and water conservation** 🌱💧
