import subprocess
import time
import sys

def main():
    print("="*60)
    print("🚀 STARTING AGROCAST TWILIO IVR MICROSERVICE...")
    print("="*60)
    
    # Start the FastAPI server via uvicorn in a subprocess
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "twilio_server:app_voice", "--host", "0.0.0.0", "--port", "8001", "--reload"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    time.sleep(2)  # Give uvicorn a moment to boot
    
    print("\n" + "#"*60)
    print("🚨 LOCAL DEPLOYMENT READY 🚨")
    print("Your Twilio Microservice is now running on http://127.0.0.1:8001")
    print("\n👉 NOW START NGROK IN A NEW TERMINAL TAB:")
    print("    ngrok http 8001")
    print("\n👉 ONCE NGROK IS RUNNING, COPY ITS HTTPS URL.")
    print("\n👉 PASTE THIS INTO THE TWILIO CONSOLE WEBHOOK URL:")
    print("    [YOUR_NGROK_URL]/voice/incoming")
    print("\n👉 TEST IT: You can verify the server is live by opening:")
    print("    http://127.0.0.1:8001/health")
    print("#"*60 + "\n")
    
    try:
        # Keep the script alive while the server runs
        server_process.wait()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()
