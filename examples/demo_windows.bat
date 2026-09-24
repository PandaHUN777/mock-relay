@echo off
start "mockrelay-demo-upstream" cmd /k python examples\demo_upstream.py
timeout /t 1 >nul
start "mockrelay-record" cmd /k mockrelay serve --mode record
timeout /t 2 >nul
curl -s http://localhost:8080/local/v1/users
echo.
echo Fixtures:
dir /b /s fixtures\local
echo.
echo Now Ctrl-C the record window and run:
echo   mockrelay serve --mode replay --latency 150
