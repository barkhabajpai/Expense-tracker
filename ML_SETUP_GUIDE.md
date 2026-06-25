# Auto Expense Categorization with ML - Setup Guide

## Overview
This expense tracker now includes AI-powered automatic expense categorization using Logistic Regression from scikit-learn.

## Features Added

### 1. **Machine Learning Backend (Python)**
- **File**: `ml_model.py` - Core ML model training and prediction
- **File**: `ml_server.py` - Flask API server for ML predictions

#### How it works:
- Trains a Logistic Regression model using TF-IDF vectorization
- Learns from existing expense descriptions and their categories
- Predicts expense categories with confidence scores
- Automatically retrains when new data is available

### 2. **Express Backend API Extensions**
- `POST /api/predict-category` - Predict category for an expense description
- `GET /api/categories` - Get all available expense categories
- Updated to call Python ML server and provide fallback handling

### 3. **Frontend Auto-Categorization**
- Real-time category prediction as user types description
- Loading indicator while prediction is happening
- Auto-fills category field if confidence > 0.4
- Smooth user experience with fallback to manual selection

## Installation & Setup

### Step 1: Install Python Dependencies
```bash
# Navigate to project directory
cd c:\Users\Nandi\OneDrive\Desktop\expense-tracker\budget-1

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Node Dependencies
```bash
npm install
```

### Step 3: Start the Services

**Terminal 1 - ML Server (Port 5001)**
```bash
python ml_server.py
```

**Terminal 2 - Express Backend (Port 5000)**
```bash
npm run server
```

**Terminal 3 - React Frontend (Port 3000)**
```bash
npm start
```

Or in one terminal, run:
```bash
# If concurrently is installed
npm run dev
```

## API Endpoints

### ML Prediction
- **POST** `/api/predict-category`
  - Request: `{ "description": "pizza lunch" }`
  - Response: `{ "category": "Food", "confidence": 0.85 }`

### Get Categories
- **GET** `/api/categories`
  - Response: `{ "categories": ["Food", "Transport", ...] }`

### Existing Endpoints
- **GET** `/api/expenses` - Get all expenses
- **POST** `/api/expenses` - Add new expense
- **PUT** `/api/expenses/:id` - Update expense
- **DELETE** `/api/expenses/:id` - Delete expense
- **GET** `/api/stats/summary` - Get expense statistics

## Technical Stack

### Backend
- **Express.js** - REST API server
- **Flask** - Python ML API server
- **scikit-learn** - Machine Learning (Logistic Regression)
- **pandas** - Data processing
- **TF-IDF Vectorizer** - Text feature extraction

### Frontend
- **React** - UI framework
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling

### ML Model Details
- **Algorithm**: Logistic Regression with TF-IDF vectorization
- **Training Data**: Expense descriptions and categories from `expenses.json`
- **Features**: 100 most important TF-IDF features
- **Confidence Threshold**: 40% (auto-fill category if > 40%)

## How the ML Model Works

1. **Training Phase** (runs on ml_server startup)
   - Reads all expenses from `expenses.json`
   - Extracts text features using TF-IDF vectorizer
   - Trains Logistic Regression classifier
   - Saves model to `expense_model.pkl`

2. **Prediction Phase** (real-time as user types)
   - Receives expense description from frontend
   - Vectorizes text using learned TF-IDF features
   - Runs through Logistic Regression model
   - Returns predicted category + confidence score
   - Frontend auto-fills if confidence is high enough

3. **Continuous Learning**
   - Model retrains whenever new expenses are added
   - Improves predictions with more data

## Troubleshooting

### ML Server won't start
- Ensure Python 3.7+ is installed
- Check all dependencies: `pip list | grep -E "flask|scikit")`
- Verify port 5001 is not in use

### Auto-prediction not working
- Check if ML server is running: `curl http://localhost:5001/api/ml-health`
- Check Express console for errors
- Ensure at least 2 expenses exist in `expenses.json`

### Model accuracy issues
- Model improves with more training data
- Add more diverse expense examples
- Restart ml_server to retrain: `python ml_server.py`

## Files Modified/Created

### New Files
- `ml_model.py` - ML model training & prediction logic
- `ml_server.py` - Flask API server
- `requirements.txt` - Python dependencies

### Modified Files
- `server.js` - Added `/api/predict-category` and `/api/categories` endpoints
- `package.json` - Added `axios` dependency
- `src/pages/ExpenseDashboard.jsx` - Added auto-categorization UI & logic

## Future Enhancements

- [ ] Support for multiple languages
- [ ] User preference learning (override predictions)
- [ ] Category confidence visualization
- [ ] Model performance metrics dashboard
- [ ] Advanced NLP features (word embeddings, BERT)
- [ ] Model versioning and A/B testing

---

**Created**: January 12, 2026
**Status**: ✅ Ready to use
