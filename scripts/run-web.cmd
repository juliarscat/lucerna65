@echo off
cd /d "%~dp0.."
node scripts\serve-local.js 1> server.web.log 2> server.web.err.log
