@echo off
cd /d "%~dp0.."
start "LUCERNA 65 API" /B scripts\run-api.cmd
start "LUCERNA 65 Web" /B scripts\run-web.cmd
echo API: http://127.0.0.1:8000/api/health
echo Web: http://127.0.0.1:4179
