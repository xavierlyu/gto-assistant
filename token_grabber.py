"""
GTO Wizard Token Grabber using Playwright

This script automatically captures the bearer token from GTO Wizard API requests.
"""

from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime


def get_gtowizard_token(headless=False, wait_time=10):
    """
    Capture bearer token from GTO Wizard by intercepting network requests
    
    Args:
        headless (bool): Run browser in headless mode
        wait_time (int): How long to wait for API calls (seconds)
    
    Returns:
        str: Bearer token if found, None otherwise
    """
    captured_token = None
    
    print("Starting Playwright browser...")
    
    try:
        with sync_playwright() as p:
            # Launch browser with additional args for stability
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                ]
            )
            
            # Create context with extra options
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            # Intercept all requests
            def handle_request(request):
                nonlocal captured_token
                
                # Check if this is an API request to gtowizard
                if 'api.gtowizard.com' in request.url:
                    headers = request.headers
                    
                    # Look for authorization header
                    if 'authorization' in headers:
                        captured_token = headers['authorization']
                        print(f"\n✓ Token captured from: {request.url}")
                        print(f"  Method: {request.method}")
            
            # Attach the request interceptor
            page.on('request', handle_request)
            
            print(f"\nNavigating to GTO Wizard...")
            print("Please wait while the page loads and makes API calls...")
            
            try:
                # Navigate to GTO Wizard
                page.goto("https://app.gtowizard.com/", wait_until="networkidle")
                
                print(f"\nWaiting {wait_time} seconds for API calls...")
                print("(If you need to login, please do so in the browser window)")
                
                # Wait for API calls to be made
                page.wait_for_timeout(wait_time * 1000)
                
                # If no token captured yet, try to trigger an API call
                if not captured_token:
                    print("\nNo token captured yet. Trying to trigger API calls...")
                    
                    # Try to click on something that might trigger an API call
                    # This depends on the site structure
                    try:
                        # Wait a bit more
                        page.wait_for_timeout(5000)
                    except:
                        pass
                
            except Exception as e:
                print(f"\nError during page navigation: {e}")
            
            finally:
                browser.close()
        
        return captured_token
        
    except Exception as e:
        print(f"\n❌ Error initializing browser: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Playwright browsers are installed: playwright install chromium")
        print("2. Try without headless mode")
        print("3. Check if another browser instance is running")
        return None


def decode_and_display_token(token):
    """
    Decode and display token information
    """
    if not token:
        print("\n❌ No token captured")
        return
    
    # Use the existing decoder from scraper.py
    try:
        import base64
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token_without_bearer = token[7:]
        else:
            token_without_bearer = token
        
        # Split and decode
        parts = token_without_bearer.split('.')
        if len(parts) != 3:
            print("Invalid JWT format")
            return
        
        payload = parts[1]
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        
        decoded = base64.urlsafe_b64decode(payload)
        payload_data = json.loads(decoded)
        
        # Display token info
        print("\n" + "="*60)
        print("TOKEN INFORMATION")
        print("="*60)
        print(f"Token Type: {payload_data.get('token_type', 'unknown')}")
        print(f"Public ID: {payload_data.get('public_id', 'unknown')}")
        print(f"Email: {payload_data.get('email', 'unknown')}")
        
        if 'iat' in payload_data:
            issued_at = datetime.fromtimestamp(payload_data['iat'])
            print(f"Issued At: {issued_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        if 'exp' in payload_data:
            expires_at = datetime.fromtimestamp(payload_data['exp'])
            print(f"Expires At: {expires_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Check if valid
            is_valid = datetime.now() < expires_at
            print(f"Token Valid: {'Yes ✓' if is_valid else 'No ✗'}")
        
        print("="*60)
        
    except Exception as e:
        print(f"\nError decoding token: {e}")


def save_token_to_file(token, filename="token.txt"):
    """
    Save token to a file
    """
    if token:
        with open(filename, "w") as f:
            f.write(token)
        print(f"\n✓ Token saved to {filename}")


def update_scraper_with_token(token):
    """
    Update the scraper.py file with the new token
    """
    if not token:
        print("\n❌ Cannot update scraper - no token provided")
        return False
    
    try:
        # Read the current scraper
        with open("scraper.py", "r") as f:
            content = f.read()
        
        # Find and replace the token
        import re
        
        # Pattern to match the Bearer token in the headers
        pattern = r'"authorization":\s*"Bearer [^"]*"'
        replacement = f'"authorization": "{token}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        # Write back
        with open("scraper.py", "w") as f:
            f.write(new_content)
        
        print("\n✓ Updated scraper.py with new token")
        return True
        
    except Exception as e:
        print(f"\n❌ Error updating scraper: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Capture GTO Wizard bearer token")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--wait", type=int, default=15, help="Seconds to wait for API calls (default: 15)")
    parser.add_argument("--update-scraper", action="store_true", help="Automatically update scraper.py with new token")
    parser.add_argument("--save", action="store_true", help="Save token to token.txt file")
    
    args = parser.parse_args()
    
    print("="*60)
    print("GTO WIZARD TOKEN GRABBER")
    print("="*60)
    
    # Get the token
    token = get_gtowizard_token(headless=args.headless, wait_time=args.wait)
    
    if token:
        print(f"\n✓ Successfully captured token!")
        print(f"\nToken: {token}")
        
        # Decode and display
        decode_and_display_token(token)
        
        # Save to file if requested
        if args.save:
            save_token_to_file(token)
        
        # Update scraper if requested
        if args.update_scraper:
            update_scraper_with_token(token)
            
    else:
        print("\n❌ Failed to capture token")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're logged into GTO Wizard in the browser")
        print("2. Try increasing wait time with --wait 30")
        print("3. Run without --headless to see what's happening")
        print("4. Navigate around the site to trigger API calls")

