import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import requests
import datetime
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math

# --- 1. INITIALIZE FLASK APP & FIREBASE ADMIN SDK ---
app = Flask(__name__)
CORS(app)

try:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://iotricity-0109-default-rtdb.firebaseio.com'
    })
    print("Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

# --- Global In-Memory Log for Analytics ---
irrigation_logs = []

# --- 2. MACHINE LEARNING MODEL SETUP ---
num_samples = 100
np.random.seed(42)
rainfall = np.random.uniform(5, 50, num_samples)
temperature = np.random.uniform(5, 30, num_samples)
soil_moisture = np.random.uniform(10, 80, num_samples)
valve_diameter = np.random.uniform(2, 12, num_samples)
soil_type = np.random.randint(1, 4, num_samples)
discharge_volume_rate = (
    2.5 * rainfall + 0.5 * temperature + 1.8 * soil_moisture + 10.0 * valve_diameter -
    5.0 * soil_type + np.random.normal(0, 15, num_samples)
)
features = np.column_stack((rainfall, temperature, soil_moisture, valve_diameter, soil_type))
target = discharge_volume_rate
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(features, target)
print("Machine Learning model trained successfully.")


# --- 3. HELPER FUNCTIONS ---
def get_weather_forecast(location="Kolkata,In"):
    api_key = "266e346a88c08a4bf1e1eba8e4caf7fe"
    base_url = "https://api.openweathermap.org/data/2.5/weather" # Changed to current weather for widget
    params = {"q": location, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        # For prediction, we still need a forecast, so we'll use a separate call or simulate it
        rainfall_forecast = 0 # Placeholder, as current weather doesn't give 3h rain forecast
        return temp, rainfall_forecast, humidity, description, None
    except requests.exceptions.RequestException as e:
        return None, None, None, None, f"API Error: {e}"
    except (KeyError, IndexError) as e:
        return None, None, None, None, f"Data Parsing Error: {e}"

def get_soil_moisture_from_firebase():
    try:
        ref = db.reference('/sensor/humidity')
        moisture = ref.get()
        if moisture is not None:
            moisture_float = float(moisture)
            status = "Dry"
            if moisture_float > 70: status = "Wet"
            elif moisture_float > 40: status = "Optimal"
            return moisture_float, status, None
        else:
            return None, None, "Data not found at '/sensor/humidity' in Firebase."
    except Exception as e:
        return None, None, f"Firebase Error: {e}"

def format_time(seconds):
    if seconds < 0: return "Invalid time"
    minutes = math.floor(seconds / 60)
    remaining_seconds = round(seconds % 60)
    return f"{minutes} min, {remaining_seconds} sec" if minutes > 0 else f"{remaining_seconds} sec"

# --- 4. FLASK ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# --- NEW API Routes for Real-time Widgets ---
@app.route('/api/weather')
def api_weather():
    temp, _, humidity, description, err = get_weather_forecast()
    if err:
        return jsonify({"temperature": None, "humidity": None, "description": "Error", "error": err}), 500
    return jsonify({"temperature": temp, "humidity": humidity, "description": description})

@app.route('/api/soil-moisture')
def api_soil_moisture():
    moisture, status, err = get_soil_moisture_from_firebase()
    if err:
        return jsonify({"moisture": None, "status": "Error", "error": err}), 500
    return jsonify({"moisture": moisture, "status": status})
# --- END of NEW API Routes ---


@app.route('/predict', methods=['POST'])
def predict():
    steps = []
    try:
        valve_diameter = float(request.form['valve_diameter'])
        soil_type_code = int(request.form['soil_type'])
        field_area = float(request.form['field_area'])
        steps.append(f"✅ Received user input: Valve Diameter = {valve_diameter}\", Soil Type = {soil_type_code}, Area = {field_area} m².")
    except (ValueError, KeyError) as e:
        return jsonify({'error': f"Invalid input form data: {e}"})

    moisture, _, err = get_soil_moisture_from_firebase()
    if err:
        steps.append(f"❌ ERROR fetching sensor data: {err}")
        return jsonify({'steps': steps, 'error': "Could not fetch soil moisture."})
    steps.append(f"✅ Successfully fetched live soil moisture: {moisture}%.")

    temp, rainfall, _, _, err = get_weather_forecast()
    if err:
        steps.append(f"❌ ERROR fetching weather forecast: {err}")
        return jsonify({'steps': steps, 'error': "Could not fetch weather forecast."})
    steps.append(f"✅ Successfully fetched weather forecast: Temp = {temp}°C, Rainfall = {rainfall} mm.")

    predicted_rate = 0
    try:
        input_features = np.array([[rainfall, temp, moisture, valve_diameter, soil_type_code]])
        steps.append(f"⚙️ Assembled feature array: {input_features.tolist()}")
        prediction = model.predict(input_features)
        predicted_rate = round(prediction[0], 2)
        if predicted_rate <= 0:
            predicted_rate = 0.1
            steps.append(f"⚠️ Model predicted non-positive rate. Clamping to {predicted_rate} m³/s.")
        steps.append(f"🤖 AI model predicted discharge rate: {predicted_rate} m³/s.")
    except Exception as e:
        steps.append(f"❌ ERROR during model prediction: {e}")
        return jsonify({'steps': steps, 'error': "Failed to run prediction model."})

    soil_type_map = {1: "Sandy", 2: "Loamy", 3: "Clay"}
    water_depth_mm = {1: 25, 2: 20, 3: 15}
    soil_name = soil_type_map.get(soil_type_code, "Unknown")
    depth_mm = water_depth_mm.get(soil_type_code, 20)
    depth_m = depth_mm / 1000
    total_volume_m3 = field_area * depth_m
    steps.append(f"💧 Calculating water for {soil_name} soil: {depth_mm}mm application over {field_area} m².")
    steps.append(f"💧 Total water volume required: {total_volume_m3:.2f} m³.")
    
    run_time_seconds = total_volume_m3 / predicted_rate
    pump_run_time_str = format_time(run_time_seconds)
    steps.append(f"⏱️ Calculated pump time: ({total_volume_m3:.2f} m³ / {predicted_rate} m³/s) = {run_time_seconds:.2f}s.")
    
    try:
        runtime_to_save = round(run_time_seconds, 2)
        runtime_ref = db.reference('/control/pump_runtime_seconds')
        runtime_ref.set(runtime_to_save)
        steps.append(f"✅ Saved runtime ({runtime_to_save}s) to Firebase for device control.")
    except Exception as e:
        steps.append(f"❌ ERROR saving runtime to Firebase: {e}")

    baseline_volume_m3 = field_area * (depth_mm * 1.5 / 1000)
    irrigation_logs.append({
        "timestamp": datetime.datetime.now(),
        "smart_volume_m3": total_volume_m3,
        "baseline_volume_m3": baseline_volume_m3
    })
    
    efficiency_percentage = (1 - (total_volume_m3 / baseline_volume_m3)) * 100 if baseline_volume_m3 > 0 else 100

    return jsonify({
        'steps': steps,
        'pump_run_time': pump_run_time_str,
        'total_volume': f"{total_volume_m3:.2f}",
        'discharge_rate': f"{predicted_rate}",
        'efficiency_percentage': round(efficiency_percentage, 2)
    })

@app.route('/stats')
def stats():
    if not irrigation_logs:
        return jsonify({ "total_water_saved": 0, "savings_percentage": 0, "chart_data": {"labels": [], "smart_usage": [], "baseline_usage": []} })

    total_smart_usage = sum(log['smart_volume_m3'] for log in irrigation_logs)
    total_baseline_usage = sum(log['baseline_volume_m3'] for log in irrigation_logs)
    total_water_saved = total_baseline_usage - total_smart_usage
    savings_percentage = (total_water_saved / total_baseline_usage * 100) if total_baseline_usage > 0 else 0
    labels = [f"Event #{i+1}" for i in range(len(irrigation_logs))]
    smart_data = [round(log['smart_volume_m3'], 2) for log in irrigation_logs]
    baseline_data = [round(log['baseline_volume_m3'], 2) for log in irrigation_logs]

    return jsonify({
        "total_water_saved": round(total_water_saved, 2),
        "savings_percentage": round(savings_percentage, 1),
        "chart_data": { "labels": labels, "smart_usage": smart_data, "baseline_usage": baseline_data }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)

