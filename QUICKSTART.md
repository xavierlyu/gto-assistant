# Quick Start Guide

Get up and running with the GTO Wizard scraper in 3 steps.

## Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Step 2: Get Your Token

**Option A: Automatic (Easiest)**
```bash
python token_grabber.py --update-scraper
```
- Browser will open
- Login to GTO Wizard if needed
- Wait for token to be captured
- Script will automatically update scraper.py

**Option B: Manual**
```bash
python token_grabber.py
```
Then copy the displayed token and paste it into `scraper.py` manually.

## Step 3: Run the Scraper

```bash
python scraper.py
```

Results will be saved to `output.json`.

---

## Full Example

```bash
# One-time setup
pip install -r requirements.txt
playwright install chromium

# Get token and update scraper
python token_grabber.py --update-scraper --save

# Run the scraper
python scraper.py
```

## Common Issues

### "No token captured"
```bash
# Try with more wait time
python token_grabber.py --wait 30 --update-scraper
```

### "playwright: command not found"
```bash
# Make sure playwright is installed
pip install playwright
playwright install chromium
```

### "Token expired"
```bash
# Get a new token
python token_grabber.py --update-scraper
```

---

## What's Next?

- Modify API parameters in `scraper.py` to get different solutions
- Set up automated token refresh for cron jobs
- Parse `output.json` to analyze GTO strategies

See `README.md` for detailed documentation.

