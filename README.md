# GTO Assistant

A Next.js web application for poker hand analysis and GTO (Game Theory Optimal) strategy assistance.

## 🎯 Overview

This project provides an AI-powered chatbot interface for analyzing poker hands and discussing GTO strategies.

## 📁 Project Structure

This is a monorepo containing:

- **`/frontend`** - Next.js web application (deployed to [rangewater.tech](https://rangewater.tech))
- **`/scraper.py`** - Data scraper utility
- **`/token_grabber*.py`** - Authentication token management tools
- **`/setup.sh`** - Quick setup script

## 🛠️ Tech Stack

### Frontend

- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **IBM Plex Mono** - Monospace font
- **Lucide React** - Icons

### Python Tools

- **Selenium** - Browser automation
- **Playwright** - Web scraping
- **Requests** - HTTP client

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/xavierlyu/gto-assistant.git
cd gto-assistant
```

### 2. Install Dependencies

```bash
# Python tools (optional)
pip install -r requirements.txt

# Frontend
cd frontend
yarn install
```

## 🚀 Usage

### Web Application

1. **Start the development server**:

   ```bash
   cd frontend
   yarn dev
   ```

2. **Open browser**: Navigate to `http://localhost:3000`

3. **Build for production**:

   ```bash
   cd frontend
   yarn build
   ```

## 🚀 Deployment

The frontend is automatically deployed to GitHub Pages at [rangewater.tech](https://rangewater.tech) via GitHub Actions.

### GitHub Pages Setup

The deployment workflow:

1. Builds the Next.js application
2. Exports static files to `out/` directory
3. Deploys to `gh-pages` branch
4. Serves at custom domain with CNAME

### Manual Deployment

```bash
cd frontend
yarn build
# Output is in frontend/out/
```

## 🧪 Development

### Project Commands

```bash
# Frontend development
cd frontend
yarn dev          # Start dev server
yarn build        # Build for production
yarn lint         # Run ESLint
```

### Python Tools

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scraper.py

# Run token grabber
python token_grabber.py
```

## 📝 Environment Variables

Create a `.env` file for any required API keys or configuration (if needed).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

- **Educational use only**
- **Use responsibly**
- Respect all applicable terms of service

## 🔗 Links

- **Live Site**: [rangewater.tech](https://rangewater.tech)
- **Repository**: [github.com/xavierlyu/gto-assistant](https://github.com/xavierlyu/gto-assistant)
