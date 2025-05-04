import pytest
from server.core.prediction import PredictionEngine
from datetime import datetime

def test_prediction_engine_initialization():
    engine = PredictionEngine()
    assert engine.thresholds['fci_signal'] == 0.7
    assert len(engine.prediction_history) == 0

def test_m_wave_detection():
    engine = PredictionEngine()
    
    # Test data with FCI signal above threshold
    test_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'fci_probe': {'signal_value': 0.8},
        'vibration': {'rms': 0.3},
        'magnetometer': {'magnitude': 50.0},
        'bme688': {
            'gas_resistance': 40000.0,
            'temperature_c': 25.0,
            'humidity_percent': 50.0,
            'pressure_hpa': 1013.25
        }
    }
    
    prediction = engine.predict(test_data)
    assert 'M_Wave_FCI' in prediction['m_wave_signals']
    assert prediction['probability'] > 0
    assert prediction['magnitude'] > 0

def test_no_m_wave_detection():
    engine = PredictionEngine()
    
    # Test data with all signals below threshold
    test_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'fci_probe': {'signal_value': 0.3},
        'vibration': {'rms': 0.2},
        'magnetometer': {'magnitude': 30.0},
        'bme688': {
            'gas_resistance': 30000.0,
            'temperature_c': 25.0,
            'humidity_percent': 50.0,
            'pressure_hpa': 1013.25
        }
    }
    
    prediction = engine.predict(test_data)
    assert len(prediction['m_wave_signals']) == 0
    assert prediction['probability'] == 10.0
    assert prediction['magnitude'] == 2.0

def test_prediction_history():
    engine = PredictionEngine()
    test_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'fci_probe': {'signal_value': 0.8},
        'vibration': {'rms': 0.3},
        'magnetometer': {'magnitude': 50.0},
        'bme688': {
            'gas_resistance': 40000.0,
            'temperature_c': 25.0,
            'humidity_percent': 50.0,
            'pressure_hpa': 1013.25
        }
    }
    
    # Make multiple predictions
    for _ in range(5):
        engine.predict(test_data)
    
    assert len(engine.prediction_history) == 5
    assert all('probability' in pred for pred in engine.prediction_history) 