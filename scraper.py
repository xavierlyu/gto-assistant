import requests
import json
import base64
from datetime import datetime

def decode_jwt_token(token):
    """
    Decode JWT token to extract payload information
    """
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Split the token into parts
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid JWT token format")
        
        # Decode the payload (second part)
        payload = parts[1]
        
        # Add padding if needed
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        
        # Decode base64
        decoded = base64.urlsafe_b64decode(payload)
        payload_data = json.loads(decoded)
        
        return payload_data
    except Exception as e:
        print(f"Error decoding JWT token: {e}")
        return None

def check_token_expiry(token):
    """
    Check if the JWT token is expired
    """
    payload = decode_jwt_token(token)
    if not payload:
        return False, "Could not decode token"
    
    # Extract expiry time
    exp_timestamp = payload.get('exp')
    if not exp_timestamp:
        return False, "No expiry time found in token"
    
    # Convert to datetime
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    current_datetime = datetime.now()
    
    is_expired = current_datetime >= exp_datetime
    
    return not is_expired, {
        'expires_at': exp_datetime.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'issued_at': datetime.fromtimestamp(payload.get('iat', 0)).strftime('%Y-%m-%d %H:%M:%S UTC'),
        'token_type': payload.get('token_type', 'unknown'),
        'public_id': payload.get('public_id', 'unknown'),
        'email': payload.get('email', 'unknown')
    }

def fetch_gtowizard_spot_solution():
    """
    Fetch spot solution data from GTO Wizard API
    """
    url = "https://api.gtowizard.com/v4/solutions/spot-solution/"
    
    # Query parameters
    params = {
        "gametype": "MTTGeneral",
        "depth": "100.125",
        "stacks": "",
        "preflop_actions": "F",
        "flop_actions": "",
        "turn_actions": "",
        "river_actions": "",
        "board": ""
    }
    
    # Headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzQ3ODUzLCJpYXQiOjE3NjEzNDY5NTMsImp0aSI6ImMwOWFhMWVhNzZiZTRmYmI5Mzk3YTVjMjY2Njg2YjQ3IiwicHVibGljX2lkIjoiYWNjXzI1ODUzZmdvMXciLCJlbWFpbCI6InhsbGdtc0BnbWFpbC5jb20ifQ.p8nJOviZ_DgHYtMMcWVJFR8u9B0WViuwoj-AykYFakI",
        "gwclientid": "1df2217a-6753-4e38-8d03-ff4f505e5b77",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://app.gtowizard.com/"
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None


if __name__ == "__main__":
    # The JWT token from the original request
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzQxNTYzLCJpYXQiOjE3NjEzNDA2NjMsImp0aSI6IjRjNTVlN2M1ZThlNjRkOTdiOWU2MGJmODc5NjhkZmQzIiwicHVibGljX2lkIjoiYWNjX2xhYmpkZWN1d3giLCJlbWFpbCI6Im1qOXQ5NHcyc3dAcHJpdmF0ZXJlbGF5LmFwcGxlaWQuY29tIn0.I5x72gvRokKfoLcFkccEERpN2uzEf0Q0xCzIJDu-SAU"
    
    # Check token status
    print("=== JWT Token Analysis ===")
    is_valid, token_info = check_token_expiry(token)
    
    if isinstance(token_info, dict):
        print(f"Token Type: {token_info['token_type']}")
        print(f"Public ID: {token_info['public_id']}")
        print(f"Email: {token_info['email']}")
        print(f"Issued At: {token_info['issued_at']}")
        print(f"Expires At: {token_info['expires_at']}")
        print(f"Token Valid: {'Yes' if is_valid else 'No'}")
    else:
        print(f"Token Error: {token_info}")
    
    print("\n" + "="*50 + "\n")
    
    if not is_valid:
        print("WARNING: Token is expired! You need to get a new token.")
        print("The API request will likely fail.")
    
    # Fetch the data
    print("Fetching data from GTO Wizard API...")
    result = fetch_gtowizard_spot_solution()
    
    if result:
        with open("output.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\nData saved to output.json")
    else:
        print("Failed to fetch data")

