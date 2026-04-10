# Start the FastAPI Backend on port 8000
Start-Process powershell -ArgumentList "-NoExit -Command "".\.venv\Scripts\Activate.ps1; uvicorn main:app --host 0.0.0.0 --port 8000"""

# Start the Twilio Voice Microservice on port 8001
Start-Process powershell -ArgumentList "-NoExit -Command "".\.venv\Scripts\Activate.ps1; python run_demo.py"""

# Start the Streamlit Frontend App
Start-Process powershell -ArgumentList "-NoExit -Command "".\.venv\Scripts\Activate.ps1; streamlit run app.py"""

Write-Host "All services started in new windows!"
