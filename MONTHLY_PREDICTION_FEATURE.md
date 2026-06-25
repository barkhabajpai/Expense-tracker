# 📊 Monthly Expense Prediction Feature

## Overview

The app now includes **AI-powered monthly expense predictions** that forecast your spending for the next month based on historical data.

## Features

### 🎯 Prediction Components

1. **Total Expense Prediction**
   - Predicts total expenses for next month
   - Shows confidence level (0-100%)
   - Based on linear regression of historical data

2. **Category-wise Predictions**
   - Individual predictions for each expense category
   - Shows trends (up/down/stable)
   - Displays historical average for comparison
   - Confidence score for each category

3. **6-Month Trend Chart**
   - Visual representation of spending patterns
   - Line chart showing monthly totals
   - Helps identify spending trends

### 🔍 How It Works

1. **Data Collection**
   - System analyzes all historical expenses from `expenses.json`
   - Groups expenses by month and category
   - Calculates trends using linear regression

2. **Prediction Algorithm**
   - Uses Linear Regression model from scikit-learn
   - Fits trend line through historical data points
   - Predicts next month value based on trend
   - Calculates R-squared as confidence metric

3. **Trend Analysis**
   - **Up**: Expenses for this category are increasing
   - **Down**: Expenses for this category are decreasing
   - **Stable**: Expenses are relatively constant

### 📈 Prediction Accuracy

**Factors affecting prediction accuracy:**
- More historical data = better predictions (minimum 2 months required)
- Consistent spending patterns = higher confidence
- Seasonal variations may reduce accuracy
- Minimum 2 months of data required

### 🚀 API Endpoints

#### Get Monthly Prediction
```http
GET http://localhost:5000/api/monthly-prediction

Response:
{
  "success": true,
  "current_month": "January 2026",
  "predicted_month": "February 2026",
  "total_prediction": 15250.50,
  "confidence": 0.85,
  "data_points": 2,
  "by_category": {
    "Food": {
      "predicted_amount": 3500,
      "trend": "up",
      "confidence": 0.92,
      "historical_avg": 3200
    },
    ...
  }
}
```

#### Get Expense Trends
```http
GET http://localhost:5000/api/expense-trends

Response:
[
  {
    "month": "2025-12",
    "total": 12500.75,
    "breakdown": {
      "Food": 2500,
      "Transport": 1200,
      ...
    }
  },
  ...
]
```

### 📊 UI Components

1. **Prediction Card** (Left Panel)
   - Shows predicted total for next month
   - Lists category-wise predictions
   - Color-coded trends
   - Displays confidence scores

2. **Trend Chart** (Right Panel)
   - 6-month expense history
   - Line chart visualization
   - Clear trend visualization
   - Interactive tooltips

### 🎲 Example Predictions

| Category | Historical Avg | Predicted | Trend | Confidence |
|----------|---|---|---|---|
| Food | ₹3,200 | ₹3,500 | ↑ Up | 92% |
| Transport | ₹1,200 | ₹1,150 | ↓ Down | 85% |
| Entertainment | ₹800 | ₹850 | ↑ Up | 78% |
| Utilities | ₹2,000 | ₹2,000 | → Stable | 95% |

### 📝 Python Implementation

**Files involved:**
- `monthly_predictor.py` - Core prediction logic
- `get_prediction.py` - Prediction API helper
- `get_trends.py` - Trends API helper
- `server.js` - Express endpoints

**Key Classes:**
- `MonthlyExpensePredictor` - Main prediction engine
  - `predict_next_month()` - Generate predictions
  - `get_expense_trends()` - Calculate trends
  - `parse_date()` - Date parsing utility
  - `get_monthly_breakdown()` - Group expenses by month

### 🧪 Testing Predictions

1. Add at least 2 months of expense data
2. View the dashboard
3. Check the "Monthly Prediction" card
4. Review category predictions
5. Analyze 6-month trend chart

### 🔧 Configuration

To adjust prediction behavior, modify in `monthly_predictor.py`:

```python
# Linear Regression parameters
model = LinearRegression()

# To use different algorithms:
# from sklearn.ensemble import RandomForestRegressor
# model = RandomForestRegressor()
```

### ⚠️ Limitations

- Requires minimum 2 months of historical data
- May not account for seasonal variations
- Large one-time expenses can skew predictions
- Confidence decreases with variable spending
- Cannot predict for new categories

### 🚀 Future Enhancements

- [ ] Seasonal adjustment for holidays/events
- [ ] Outlier detection and handling
- [ ] Weekly predictions for shorter cycles
- [ ] Custom prediction models
- [ ] What-if scenario planning
- [ ] Budget recommendations based on predictions
- [ ] Anomaly detection (unusual spending)

### 💡 Tips for Better Predictions

1. **Consistent Categories** - Use same category names consistently
2. **Detailed Descriptions** - Better for auto-categorization
3. **Regular Updates** - Add expenses as they occur
4. **Long History** - More data = better predictions
5. **Monitor Trends** - Watch for spending pattern changes

---

**Status**: ✅ Ready to Use
**Version**: 1.0.0
**Date**: January 12, 2026
