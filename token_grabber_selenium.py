#!/usr/bin/env python3
"""
GTO Wizard Token Grabber using Selenium (More stable on macOS)

This is a fallback option when Playwright doesn't work.
"""

import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def auto_login_google(driver, email='xllgms@gmail.com', password=None):
    """
    Automatically login to GTO Wizard using Google
    
    Args:
        driver: Selenium WebDriver instance
        email: Google email for login (or use GTO_EMAIL env var)
        password: Google password for login (or use GTO_PASSWORD env var)
    
    Returns:
        bool: True if login successful, False otherwise
    """
    try:
        # Get credentials from parameters or environment variables
        email = email or os.getenv('GTO_EMAIL', 'xllgms@gmail.com')
        password = password or os.getenv('GTO_PASSWORD', '1234567890')
        
        if not email or not password:
            print("⚠️  No credentials provided. Skipping auto-login.")
            print("   Set GTO_EMAIL and GTO_PASSWORD env vars for auto-login")
            return False
        
        print("\n🔐 Attempting Google login...")
        
        # Wait for login page to load
        wait = WebDriverWait(driver, 10)
        
        # Find and click Google login button (contains text "GOOGLE")
        try:
            google_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'GOOGLE')]"))
            )
            print("   Found Google login button")
            google_button.click()
            time.sleep(3)
            
            # Handle Google OAuth popup/tab
            print("   Waiting for Google sign-in popup...")
            time.sleep(5)
            
            # Try to find the Google sign-in page (could be new tab or existing window)
            # First, check if we're already on the Google sign-in page
            try:
                # Check current URL for Google accounts
                if 'accounts.google.com' in driver.current_url:
                    print("   Already on Google sign-in page")
                else:
                    # Wait for new window/tab to open
                    original_window = driver.current_window_handle
                    wait.until(lambda d: len(d.window_handles) > 1 or 'accounts.google.com' in d.current_url)
                    
                    # Switch to new window if it opened
                    windows = driver.window_handles
                    if len(windows) > 1:
                        driver.switch_to.window(windows[-1])
                        print("   Switched to Google sign-in window")
                    else:
                        print("   Google opened in same window")
                
                # Enter Google email
                email_field = wait.until(
                    EC.presence_of_element_located((By.ID, "identifierId"))
                )
                email_field.send_keys(email)
                print("   Entered email")
                
                # Click next
                next_btn = driver.find_element(By.ID, "identifierNext")
                next_btn.click()
                time.sleep(3)
                
                # Enter Google password
                password_field = wait.until(
                    EC.presence_of_element_located((By.NAME, "Passwd"))
                )
                password_field.send_keys(password)
                print("   Entered password")
                
                # Click next to sign in
                next_btn = driver.find_element(By.ID, "passwordNext")
                next_btn.click()
                print("   Submitted login form")
                time.sleep(5)
                
                # Handle 2FA if needed (will pause here)
                # User can manually enter 2FA code if required
                
                # Wait for redirect back to GTO Wizard
                if len(windows) > 1:
                    # If we switched windows, switch back
                    driver.switch_to.window(windows[0])
                else:
                    # Wait for redirect to GTO Wizard
                    time.sleep(3)
                
                print("✅ Google login successful!")
                return True
                    
            except Exception as e:
                print(f"   Google sign-in flow failed: {e}")
                print("   You may need to handle 2FA manually")
                # Try to switch back to original window
                try:
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return False
                
        except Exception as e:
            print(f"   Could not find Google login button: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Auto-login failed: {e}")
        return False


def get_gtowizard_token_selenium(wait_time=15, email=None, password=None, auto_login_enabled=True):
    """
    Capture bearer token using Selenium with Chrome DevTools Protocol
    
    Args:
        wait_time (int): How long to wait for API calls (seconds)
    
    Returns:
        str: Bearer token if found, None otherwise
    """
    print("Starting Chrome browser with Selenium...")
    
    captured_token = None
    
    # Setup Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment for headless mode
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--start-maximized')
    
    # Enable logging of network events
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    driver = None
    
    try:
        # Create driver
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"\nNavigating to GTO Wizard...")
        driver.get("https://app.gtowizard.com/")
        
        time.sleep(3)
        
        # Try automatic Google login if enabled
        if auto_login_enabled:
            login_success = auto_login_google(driver, email, password)
            if not login_success:
                print(f"\n⚠️  Manual login required.")
                print(f"   Please login in the browser window...")
                print(f"   Waiting {wait_time} seconds...")
        else:
            print(f"\nWaiting {wait_time} seconds for you to interact with the site...")
            print("Please login if needed, then navigate around to trigger API calls...")
        
        # Wait for user interaction and API calls
        time.sleep(wait_time)
        
        print("\nChecking network logs for authorization tokens...")
        
        # Get performance logs (network activity)
        logs = driver.get_log('performance')
        
        # Parse logs to find authorization headers
        for log in logs:
            try:
                log_entry = json.loads(log['message'])
                message = log_entry.get('message', {})
                method = message.get('method', '')
                
                # Look for network requests
                if method == 'Network.requestWillBeSent':
                    params = message.get('params', {})
                    request = params.get('request', {})
                    headers = request.get('headers', {})
                    url = request.get('url', '')
                    
                    # Check if this is a GTO Wizard API request
                    if 'api.gtowizard.com' in url:
                        # Look for authorization header (case-insensitive)
                        for header_name, header_value in headers.items():
                            if header_name.lower() == 'authorization':
                                captured_token = header_value
                                print(f"\n✓ Token captured from: {url}")
                                break
                    
                    if captured_token:
                        break
                        
            except Exception as e:
                # Skip invalid log entries
                continue
        
        return captured_token
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome/Chromium is installed")
        print("2. Install ChromeDriver: brew install chromedriver")
        print("3. Or download from: https://chromedriver.chromium.org/")
        return None
        
    finally:
        if driver:
            driver.quit()


def decode_and_display_token(token):
    """
    Decode and display token information (same as playwright version)
    """
    if not token:
        print("\n❌ No token captured")
        return
    
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
    
    parser = argparse.ArgumentParser(description="Capture GTO Wizard bearer token using Selenium")
    parser.add_argument("--wait", type=int, default=20, help="Seconds to wait for API calls (default: 20)")
    parser.add_argument("--update-scraper", action="store_true", help="Automatically update scraper.py with new token")
    parser.add_argument("--save", action="store_true", help="Save token to token.txt file")
    parser.add_argument("--email", type=str, help="Email for auto-login (or set GTO_EMAIL env var)")
    parser.add_argument("--password", type=str, help="Password for auto-login (or set GTO_PASSWORD env var)")
    parser.add_argument("--no-auto-login", action="store_true", help="Disable automatic login")
    
    args = parser.parse_args()
    
    print("="*60)
    print("GTO WIZARD TOKEN GRABBER (Google Login)")
    print("="*60)
    
    # Check for auto-login credentials
    if not args.no_auto_login and (args.email or os.getenv('GTO_EMAIL')):
        print("\n🔐 Google auto-login enabled")
        print("   Script will attempt to login with Google automatically")
    else:
        print("\nIMPORTANT:")
        print("- A Chrome window will open")
        print("- Click the GOOGLE login button manually")
        print("- Navigate around the site (click on solver, etc.)")
        print("- This triggers API calls that contain the token")
    
    print("="*60)
    
    # Get the token
    token = get_gtowizard_token_selenium(
        wait_time=args.wait,
        email=args.email,
        password=args.password,
        auto_login_enabled=not args.no_auto_login
    )
    
    if token:
        print(f"\n✓ Successfully captured token!")
        print(f"\nToken: {token}")
        
        # Decode and display
        decode_and_display_token(token)
        
        # Save to file if requested
        if args.save:
            with open("token.txt", "w") as f:
                f.write(token)
            print(f"\n✓ Token saved to token.txt")
        
        # Update scraper if requested
        if args.update_scraper:
            update_scraper_with_token(token)
            
    else:
        print("\n❌ Failed to capture token")
        print("\nTips:")
        print("1. Make sure you interact with the site during the wait time")
        print("2. Click on 'Solver' or 'Solutions' to trigger API calls")
        print("3. Try increasing wait time: --wait 30")
        print("4. Check if you're logged in to GTO Wizard")

