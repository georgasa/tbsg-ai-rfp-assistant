# Quick Setup Guide

## Files Created

1. **`intelligent_rag_client.py`** - Intelligent client with automated follow-up questions
2. **`advanced_intelligent_client.py`** - Advanced intelligent client with sophisticated analysis
3. **`requirements.txt`** - Python dependencies
4. **`README.md`** - Comprehensive documentation
5. **`run_intelligent_client.bat`** - Windows batch file for intelligent client
6. **`run_advanced_client.bat`** - Windows batch file for advanced client
7. **`SETUP_INSTRUCTIONS.md`** - This quick setup guide

## Quick Start

### Option 1: Web Application (Recommended)
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

4. **Access the web interface**:
   - Open http://localhost:5000 in your browser

### Option 2: Docker Compose (Full Stack)
1. **Start with nginx reverse proxy**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - HTTP: http://localhost
   - HTTPS: https://localhost (if SSL certificates are configured)

### Option 3: Command Line Clients
1. **Run the intelligent client**:
   ```bash
   python intelligent_rag_client.py
   ```
   
   Or on Windows, double-click `run_intelligent_client.bat`

2. **Run the advanced intelligent client**:
   ```bash
   python advanced_intelligent_client.py
   ```
   
   Or on Windows, double-click `run_advanced_client.bat`

## Features

### Intelligent Client
- ✅ Automated follow-up question generation
- ✅ Interactive command-line interface
- ✅ JWT authentication with your provided token
- ✅ Multi-region support (Global, MEA, US)
- ✅ Comprehensive model selection
- ✅ Error handling and connection testing
- ✅ Conversation history saving
- ✅ User controls (quit, skip, manual questions)

### Advanced Intelligent Client
- ✅ Sophisticated topic analysis and extraction
- ✅ Advanced topic coverage tracking
- ✅ Uncovered areas detection
- ✅ Enhanced user controls
- ✅ Progress tracking and conversation summary
- ✅ All features from the basic intelligent client

## JWT Token Configuration

The program uses a **single source of truth** for JWT token configuration:

### Python Client
- **File**: `shared_config.py` (line 70)
- **Current Token**: Configured and working ✅

### Android App  
- **File**: `android-app/app/src/main/java/com/temenos/ragclient/data/SharedConfig.kt` (line 72)
- **Current Token**: Synchronized with Python client ✅

### Token Expiration
Your current token expires on **October 3, 2025**. When it expires, update it in both files to maintain consistency across platforms.

## Usage Examples

### Intelligent Client
```bash
python intelligent_rag_client.py
```

### Advanced Intelligent Client
```bash
python advanced_intelligent_client.py
```

### Example Conversation Flow
1. Enter your initial question
2. The client will automatically generate 5 follow-up questions
3. Use controls:
   - `Enter` - Ask the current question
   - `s` - Skip to next question
   - `q` - Quit automation
   - `m` - Enter manual question (advanced client only)

## Support

- Check the `README.md` for detailed documentation
- Run the intelligent clients to explore available models
- Conversation history is automatically saved to JSON files

Enjoy exploring the Temenos knowledge base with intelligent automation! 🚀🤖 