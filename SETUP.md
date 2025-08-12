# 🚀 Quick Setup Guide

## Prerequisites

- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

## 🎯 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your API keys
# - OPENROUTER_API_KEY: Get from https://openrouter.ai/
# - Gmail credentials: Follow Gmail API setup below
```

### 3. Start the System

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
./start.sh
```

**Manual:**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

## 🔑 API Setup

### OpenRouter API Key
1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up and get your API key
3. Add to `.env` file: `OPENROUTER_API_KEY=sk-or-...`

### Gmail API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download `credentials.json` to `backend/credentials/`
6. Run app and complete OAuth flow

## 🌐 Access Points

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🐳 Docker Alternative

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t smart-email-classifier .
docker run -p 5000:5000 smart-email-classifier
```

## 🧪 Test the System

### Test Email Classification
```bash
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "I need help with my order",
    "email_subject": "Order Issue"
  }'
```

### Test Gmail Integration
```bash
curl -X POST http://localhost:5000/api/gmail/fetch
```

## 🔧 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Python dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Node dependencies:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Gmail authentication:**
- Ensure `credentials.json` is in `backend/credentials/`
- Check OAuth scopes include Gmail permissions
- Verify redirect URIs in Google Cloud Console

### Logs

- **Backend logs**: Check terminal running Flask app
- **Frontend logs**: Check browser console and terminal
- **Database**: Check `backend/emails.db` file

## 📚 Next Steps

1. **Train the Model**: Use the dashboard to retrain with your data
2. **Customize Responses**: Edit response templates in Settings
3. **Monitor Performance**: Check Analytics dashboard
4. **Scale Up**: Deploy to production with Docker/Kubernetes

## 🆘 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [API endpoints](README.md#testing) for testing
- Open an issue on GitHub for bugs
- Check logs for error details

---

**Happy Classifying! 🎉** 