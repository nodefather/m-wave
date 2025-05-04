from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from server.core.serial_manager import SerialManager
from server.core.data_processor import DataProcessor
from server.core.prediction import PredictionEngine

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
serial_manager = SerialManager()
data_processor = DataProcessor()
prediction_engine = PredictionEngine()

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Get raw data from serial
        raw_data = serial_manager.get_latest_data()
        
        # Process the data
        processed_data = data_processor.process(raw_data)
        
        # Make predictions
        predictions = prediction_engine.predict(processed_data)
        
        return jsonify({
            'status': 'success',
            'data': processed_data,
            'predictions': predictions,
            'timestamp': data_processor.get_timestamp()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'services': {
            'serial': serial_manager.is_healthy(),
            'processor': data_processor.is_healthy(),
            'prediction': prediction_engine.is_healthy()
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', False)) 