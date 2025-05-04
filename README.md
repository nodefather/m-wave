# M-WAVE: Mycelium-based Earthquake Detection System

A full-stack, multi-sensor, real-time earthquake prediction system using ESP32, Python, and a web dashboard.

## Quickstart

1. Install dependencies:
   `powershell
   .\install.ps1
   `

2. Start the development server:
   `powershell
   docker-compose up
   `

3. Open http://localhost:5000 in your browser

## Project Structure

- server/: Python Flask backend
- irmware/: ESP32 Arduino code
- web/: React/Next.js frontend
- docs/: Documentation
- 	ests/: Test suite

## Development

- Backend: poetry run python server/main.py
- Frontend: cd web && npm run dev
- Firmware: Use PlatformIO in VSCode

## Deployment

- Docker: docker-compose up -d
- Cloud: See docs/DEPLOYMENT.md
