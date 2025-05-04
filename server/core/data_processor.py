import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any
import logging

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_buffer = []
        self.max_buffer_size = 1000
        self.timestamp = datetime.utcnow()

    def process(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Update timestamp
            self.timestamp = datetime.utcnow()

            # Add to buffer
            self.data_buffer.append(raw_data)
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)

            # Process BME688 data
            bme_data = self._process_bme688(raw_data.get('bme688', {}))

            # Process magnetometer data
            mag_data = self._process_magnetometer(raw_data.get('magnetometer', {}))

            # Process vibration data
            vib_data = self._process_vibration(raw_data.get('vibration', 0))

            # Process FCI probe data
            fci_data = self._process_fci(raw_data.get('fci_probe', {}))

            return {
                'timestamp': self.timestamp.isoformat(),
                'bme688': bme_data,
                'magnetometer': mag_data,
                'vibration': vib_data,
                'fci_probe': fci_data,
                'raw': raw_data
            }
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            return {
                'timestamp': self.timestamp.isoformat(),
                'error': str(e)
            }

    def _process_bme688(self, data: Dict[str, float]) -> Dict[str, float]:
        return {
            'temperature_c': data.get('temperature_c', 0.0),
            'humidity_percent': data.get('humidity_percent', 0.0),
            'pressure_hpa': data.get('pressure_hpa', 0.0),
            'gas_resistance': data.get('gas_resistance', 0.0)
        }

    def _process_magnetometer(self, data: Dict[str, float]) -> Dict[str, float]:
        return {
            'x': data.get('x', 0.0),
            'y': data.get('y', 0.0),
            'z': data.get('z', 0.0),
            'magnitude': np.sqrt(
                data.get('x', 0.0)**2 +
                data.get('y', 0.0)**2 +
                data.get('z', 0.0)**2
            )
        }

    def _process_vibration(self, data: float) -> Dict[str, float]:
        return {
            'raw': data,
            'normalized': data / 4095.0,  # Assuming 12-bit ADC
            'rms': np.sqrt(np.mean([d.get('vibration', 0)**2 for d in self.data_buffer[-10:]]))
        }

    def _process_fci(self, data: Dict[str, float]) -> Dict[str, float]:
        return {
            'signal_value': data.get('signal_value', 0.0),
            'normalized': data.get('signal_value', 0.0) / 4095.0,
            'moving_avg': np.mean([d.get('fci_probe', {}).get('signal_value', 0.0) for d in self.data_buffer[-10:]])
        }

    def get_timestamp(self) -> str:
        return self.timestamp.isoformat()

    def is_healthy(self) -> bool:
        return len(self.data_buffer) > 0 