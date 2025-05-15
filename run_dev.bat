@echo off
echo Starting Development Environment...

:: Start Django backend server
start cmd /k "echo Starting Django Backend Server... && python manage.py runserver 0.0.0.0:8000"

:: Wait for backend to start
timeout /t 5

:: Start frontend development server (if using a separate frontend framework)
:: start cmd /k "echo Starting Frontend Development Server... && cd frontend && npm start"

echo Development environment is ready!
echo Backend URL: http://localhost:8000
echo Frontend URL: http://localhost:8000 (integrated with Django) 