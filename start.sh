#!/bin/bash

echo "🚀 Минималистичный блог - Quick Start"
echo "======================================"

# Backend setup
echo "📦 Backend dependencies installation..."
cd backend
pip3 install -r requirements.txt
echo "✅ Backend dependencies installed"

# Frontend setup
echo "📦 Frontend dependencies installation..."
cd ../frontend
pnpm install
echo "✅ Frontend dependencies installed"

# Start servers
echo "🌐 Starting servers..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Start backend in background
cd ../backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
pnpm dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 