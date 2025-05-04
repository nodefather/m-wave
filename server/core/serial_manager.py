import serial
import json
import time
from typing import Dict, Optional
import logging

class SerialManager:
    def __init__(self, port: str = "COM3", baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None
        self.latest_data = {}
        self.is_connected = False
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=1)
            self.is_connected = True
            self.logger.info(f"Connected to {self.port} at {self.baud_rate} baud")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to {self.port}: {str(e)}")
            return False

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.is_connected = False
            self.logger.info(f"Disconnected from {self.port}")

    def read_data(self) -> Optional[Dict]:
        if not self.is_connected:
            if not self.connect():
                return None

        try:
            line = self.serial.readline().decode('utf-8').strip()
            if not line:
                return None

            data = json.loads(line)
            self.latest_data = data
            return data
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON received: {line}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading from serial: {str(e)}")
            self.disconnect()
            return None

    def get_latest_data(self) -> Dict:
        return self.latest_data

    def is_healthy(self) -> bool:
        return self.is_connected

    def __del__(self):
        self.disconnect() 