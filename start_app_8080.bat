@echo off
title CI/CD DevOps Project - Running on Port 8080
echo ======================================================================
echo  Starting Application on Port 8080...
echo ======================================================================
echo.
echo  1. Keep this black terminal window OPEN.
echo  2. Open your web browser and navigate to:
echo.
echo       http://localhost:8080
echo.
echo ======================================================================
set PORT=8080
python app.py
pause
