from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
app = Flask(__name__)

# Load the trained model
model = joblib.load("hotel_booking_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Convert data into a DataFrame
        df = pd.DataFrame([data])
        
        # Make prediction
        prediction = model.predict(df)[0]  # 0 (Not Canceled) or 1 (Canceled)
        
        # Return prediction in JSON response
        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT dynamically
    app.run(host="0.0.0.0", port=port, debug=True)
