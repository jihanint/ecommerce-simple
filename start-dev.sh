#!/bin/bash

# Start backend in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"

# Wait for backend to be ready
sleep 2

# Start frontend in background
npm run dev --prefix frontend &
FRONTEND_PID=$!
echo "Frontend started with PID $FRONTEND_PID"

# Print status
echo "Both services started:"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:5173"

# Wait for both processes to complete or be terminated
wait
