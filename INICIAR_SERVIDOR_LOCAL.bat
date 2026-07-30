@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo  LUCERNA 65 - servidor local
echo ============================================
echo.

if not exist ".\.venv\Scripts\python.exe" (
  echo No trobo .\.venv\Scripts\python.exe
  echo Crea o reinstal.la l'entorn abans d'iniciar el servidor.
  echo.
  pause
  exit /b 1
)

where node >nul 2>nul
if errorlevel 1 (
  echo No trobo Node.js al PATH.
  echo Instal.la Node.js o obre el projecte des d'un terminal amb Node disponible.
  echo.
  pause
  exit /b 1
)

echo Obrint API a http://127.0.0.1:8000
start "LUCERNA 65 API" cmd /k ".\.venv\Scripts\python.exe -m uvicorn api.analyze:app --host 127.0.0.1 --port 8000"

echo Obrint web a http://127.0.0.1:4179
start "LUCERNA 65 Web" cmd /k "node scripts\serve-local.js"

timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:4179"

echo.
echo Si vols aturar el servidor, tanca les dues finestres:
echo - LUCERNA 65 API
echo - LUCERNA 65 Web
echo.
pause
