# Deepshiva Project

This project contains a Frontend, Backend, and AI Engine.

## Prerequisites
- Node.js & npm
- Python 3.8+

## 1. Backend (Express.js)
The backend handles API requests, authentication, and database connections.
```bash
cd backend
npm install
npm start
```
*Runs on: http://localhost:5000*  
*(Make sure to configure `.env` with `MONGO_URI`)*

## 2. Frontend (React)
The user interface.
```bash
cd frontend
npm install
npm start
```
*Runs on: http://localhost:3000*

## 3. AI Server (FastAPI)
Handles main AI logic, chat, and other services.
```bash
# From the project root
pip install -r requirements.txt
python ai_server.py
```
*Runs on: http://localhost:8000*

## 4. Yoga Server (Flask)
A standalone server for Yoga pose detection (TFLite safe mode for Windows).
```bash
# From the project root
python ai_engine/yoga_server.py
```
*Runs on: http://localhost:5005*
