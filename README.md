# 🧠 Smart Email Classifier with AI

An intelligent email classification and routing system that automatically analyzes incoming emails using Natural Language Processing (NLP), categorizes them into predefined business types, and triggers appropriate actions such as auto-responses and internal routing.

## ✨ Features

- **🤖 AI-Powered Classification**: Uses BERT transformers for high-accuracy email categorization
- **📧 Gmail Integration**: Seamless connection with Gmail API for real-time email processing
- **💬 Smart Auto-Responses**: Generates context-aware replies using OpenRouter LLMs
- **📊 Real-time Analytics**: Comprehensive dashboard with performance metrics and insights
- **🔄 Feedback Loop**: Continuous model improvement through user corrections
- **🎯 Business Categories**: Support, Sales, Complaints, Feedback, General Inquiry
- **📱 Modern Web Interface**: Beautiful React dashboard with real-time updates
- **🐳 Docker Ready**: Easy deployment with Docker and docker-compose

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gmail API    │    │  Flask Backend   │    │  React Frontend │
│                 │◄──►│                  │◄──►│                 │
│ • Fetch Emails │    │ • ML Pipeline    │    │ • Dashboard     │
│ • Send Replies │    │ • Gmail Service  │    │ • Email List    │
└─────────────────┘    │ • LLM Service   │    │ • Analytics     │
                       └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │  OpenRouter API  │
                       │                  │
                       │ • Llama 2        │
                       │ • Mistral        │
                       │ • Claude         │
                       └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (optional)
- Gmail API credentials
- OpenRouter API key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-email-classifier.git
cd smart-email-classifier
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENROUTER_API_KEY="your-api-key-here"
export SECRET_KEY="your-secret-key-here"

# Run the backend
cd backend
python app.py
```

### 3. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

### 4. Docker Deployment (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run individually
docker build -t smart-email-classifier .
docker run -p 5000:5000 smart-email-classifier
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development

# Gmail API
GMAIL_CREDENTIALS_FILE=path/to/credentials.json

# OpenRouter API
OPENROUTER_API_KEY=sk-or-your-api-key-here

# Database
DATABASE_URL=sqlite:///emails.db
```

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download `credentials.json` and place in `backend/credentials/`
6. Run the application and complete OAuth flow

### OpenRouter Setup

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key
3. Add to environment variables
4. Choose your preferred model (Llama 2, Mistral, Claude)

## 📊 Usage

### Dashboard Overview

- **Real-time Statistics**: Total emails, classification accuracy, response times
- **Quick Actions**: Fetch new emails, retrain model, test classification
- **Recent Activity**: Latest classified emails with confidence scores

### Email Management

- **View All Emails**: Paginated list with search and filtering
- **Category Management**: Edit classifications and confidence scores
- **Export Data**: Download email data in CSV/JSON format

### Analytics & Insights

- **Category Distribution**: Pie charts showing email volume by type
- **Performance Metrics**: Confidence scores and accuracy trends
- **Model Health**: Training data statistics and improvement suggestions

### Settings & Configuration

- **General Settings**: Auto-response toggle, confidence thresholds
- **Gmail Integration**: API credentials, label monitoring
- **AI Configuration**: Model selection, API key management

## 🧪 Testing

### Test Email Classification

```bash
# Using curl
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "I need help with my order",
    "email_subject": "Order Issue"
  }'
```

### Test Gmail Integration

```bash
# Fetch new emails
curl -X POST http://localhost:5000/api/gmail/fetch
```

### Test Model Retraining

```bash
# Retrain with new data
curl -X POST http://localhost:5000/api/model/retrain
```

## 📈 Performance

- **Classification Accuracy**: >85% F1-score with BERT model
- **Response Time**: <2 seconds for email classification
- **Auto-response Generation**: <5 seconds with OpenRouter API
- **Scalability**: Handles 1000+ emails per hour

## 🔒 Security Features

- OAuth2 authentication for Gmail API
- Secure API key management
- Input validation and sanitization
- CORS protection
- Rate limiting (configurable)

## 🚀 Deployment

### Production Deployment

```bash
# Build production image
docker build -t smart-email-classifier:prod .

# Run with production environment
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret \
  -e OPENROUTER_API_KEY=your-api-key \
  smart-email-classifier:prod
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smart-email-classifier
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smart-email-classifier
  template:
    metadata:
      labels:
        app: smart-email-classifier
    spec:
      containers:
      - name: classifier
        image: smart-email-classifier:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for BERT models
- [OpenRouter](https://openrouter.ai/) for LLM access
- [Gmail API](https://developers.google.com/gmail/api) for email integration
- [React](https://reactjs.org/) and [Tailwind CSS](https://tailwindcss.com/) for the frontend

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/m7madawawdeh/smart-email-classifier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/m7madawawdeh/smart-email-classifier/discussions)
- **Email**: moh.jameel1221@gmail.com

---

**Made with ❤️ and AI** - Automating email management for the modern business 