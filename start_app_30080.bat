@echo off
echo ========================================================
echo  Starting Application on Port 30080 (Simulated K8s NodePort)...
echo  Open your browser at: http://localhost:30080
echo  Press Ctrl+C to stop.
echo ========================================================
set PORT=30080
python app.py
pause
