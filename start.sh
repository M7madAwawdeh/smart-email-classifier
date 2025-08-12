#!/bin/bash

echo ""
echo "🧠 Smart Email Classifier with AI"
echo "===================================="
echo ""

echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "🔍 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

echo "🔍 Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo "✅ All dependencies found!"
echo ""

echo "🚀 Starting Smart Email Classifier..."
echo ""

echo "📱 Frontend will be available at: http://localhost:3000"
echo "🔧 Backend will be available at: http://localhost:5000"
echo ""

echo "Press Ctrl+C to stop all services"
echo ""

# Start the Python startup script
python3 start.py 