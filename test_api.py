import requests
import json

def test_prediction_api():
    """
    Sends a test POST request to the local AgroCast /predict endpoint.
    Uses realistic dummy data for a Tomato farmer in Coimbatore.
    """
    url = "http://127.0.0.1:8000/predict"
    
    # Coordinates for Coimbatore, Tamil Nadu
    # Realistic dummy data for Tomato farming
    payload = {
        "lat": 11.0168,
        "lon": 76.9558,
        "crop": "Tomato",
        "yield_amount": 2500.0,      # Expected yield in kg
        "current_price": 40.0,       # Local price per kg
        "distant_market_price": 55.0, # Distant market price (e.g., Chennai) per kg
        "transport_cost": 15000.0    # Cost to transport yield to distant market
    }

    print(f"Sending POST request to {url}...")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")

    try:
        response = requests.post(url, json=payload, timeout=60) # High timeout for LLM generation
        
        print(f"HTTP Status Code: {response.status_code}\n")
        
        # Parse and print formatted JSON response
        if response.headers.get('content-type') == 'application/json':
            print("Response JSON:")
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            print("Response Text:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")

if __name__ == "__main__":
    test_prediction_api()
