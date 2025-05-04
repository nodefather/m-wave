import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime, timedelta

class PredictionEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.thresholds = {
            'fci_signal': 0.7,
            'vibration_rms': 0.5,
            'mag_magnitude': 100.0,
            'gas_resistance': 50000.0
        }
        self.prediction_history = []
        self.max_history = 100

    def predict(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Extract features
            features = self._extract_features(processed_data)

            # Detect M-Wave signals
            m_wave_signals = self._detect_m_wave(features)

            # Predict earthquake event
            probability, magnitude, depth, location, predicted_time = self._predict_earthquake(
                features, m_wave_signals
            )

            # Update history
            self._update_history({
                'timestamp': processed_data['timestamp'],
                'probability': probability,
                'magnitude': magnitude,
                'signals': m_wave_signals
            })

            return {
                'm_wave_signals': m_wave_signals,
                'probability': probability,
                'magnitude': magnitude,
                'depth_km': depth,
                'location': location,
                'predicted_time_utc': predicted_time.isoformat(),
                'features': features
            }
        except Exception as e:
            self.logger.error(f"Error making prediction: {str(e)}")
            return {
                'error': str(e),
                'm_wave_signals': [],
                'probability': 0.0,
                'magnitude': 0.0,
                'depth_km': 0.0,
                'location': {'latitude': 0.0, 'longitude': 0.0},
                'predicted_time_utc': datetime.utcnow().isoformat()
            }

    def _extract_features(self, data: Dict[str, Any]) -> Dict[str, float]:
        return {
            'fci_signal': data['fci_probe']['signal_value'],
            'vibration_rms': data['vibration']['rms'],
            'mag_magnitude': data['magnetometer']['magnitude'],
            'gas_resistance': data['bme688']['gas_resistance'],
            'temperature': data['bme688']['temperature_c'],
            'humidity': data['bme688']['humidity_percent'],
            'pressure': data['bme688']['pressure_hpa']
        }

    def _detect_m_wave(self, features: Dict[str, float]) -> List[str]:
        signals = []
        
        if features['fci_signal'] > self.thresholds['fci_signal']:
            signals.append('M_Wave_FCI')
        
        if features['vibration_rms'] > self.thresholds['vibration_rms']:
            signals.append('M_Wave_Vibration')
        
        if features['mag_magnitude'] > self.thresholds['mag_magnitude']:
            signals.append('M_Wave_Magnetic')
        
        if features['gas_resistance'] > self.thresholds['gas_resistance']:
            signals.append('M_Wave_Gas')

        return signals

    def _predict_earthquake(
        self, features: Dict[str, float], signals: List[str]
    ) -> Tuple[float, float, float, Dict[str, float], datetime]:
        # Simple heuristic-based prediction
        # In production, replace with ML model
        if 'M_Wave_FCI' in signals:
            probability = 78.653
            magnitude = 6.4
            depth = 8.5
            location = {'latitude': 32.7157, 'longitude': -117.1611}
            predicted_time = datetime.utcnow() + timedelta(hours=9)
        else:
            probability = 10.0
            magnitude = 2.0
            depth = 5.0
            location = {'latitude': 0.0, 'longitude': 0.0}
            predicted_time = datetime.utcnow() + timedelta(days=1)

        return probability, magnitude, depth, location, predicted_time

    def _update_history(self, prediction: Dict[str, Any]):
        self.prediction_history.append(prediction)
        if len(self.prediction_history) > self.max_history:
            self.prediction_history.pop(0)

    def is_healthy(self) -> bool:
        return len(self.prediction_history) > 0 