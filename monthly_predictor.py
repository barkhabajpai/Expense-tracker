import json
import os
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
from collections import defaultdict

class MonthlyExpensePredictor:
    def __init__(self, expenses_file='expenses.json'):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.expenses_file = os.path.join(self.script_dir, expenses_file)
    
    def load_expenses(self):
        """Load expenses from JSON file"""
        try:
            if os.path.exists(self.expenses_file):
                with open(self.expenses_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading expenses: {e}")
            return []
    
    def parse_date(self, date_str):
        """Parse date string - handles multiple formats"""
        try:
            # Try MM/DD/YYYY format
            if '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 3:
                    month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                    # Handle 2-digit years
                    if year < 100:
                        year = 2000 + year if year < 50 else 1900 + year
                    return datetime(year, month, day)
        except:
            pass
        
        try:
            # Fallback to ISO format
            return datetime.fromisoformat(date_str)
        except:
            return None
    
    def get_monthly_breakdown(self):
        """Get expenses grouped by month and category"""
        expenses = self.load_expenses()
        monthly_data = defaultdict(lambda: defaultdict(float))
        
        for expense in expenses:
            date_obj = self.parse_date(expense.get('date', ''))
            if date_obj:
                month_key = f"{date_obj.year}-{date_obj.month:02d}"
                category = expense.get('category', 'Other')
                amount = float(expense.get('amount', 0))
                monthly_data[month_key][category] += amount
        
        return dict(monthly_data)
    
    def predict_next_month(self):
        """Predict expenses for next month"""
        expenses = self.load_expenses()
        
        if not expenses:
            return {
                'error': 'No historical data',
                'prediction': None,
                'confidence': 0
            }
        
        # Group by month and category
        monthly_breakdown = self.get_monthly_breakdown()
        
        if len(monthly_breakdown) < 2:
            return {
                'error': 'Insufficient data - need at least 2 months',
                'prediction': None,
                'confidence': 0
            }
        
        # Sort months
        sorted_months = sorted(monthly_breakdown.keys())
        
        # Get all categories
        all_categories = set()
        for month_data in monthly_breakdown.values():
            all_categories.update(month_data.keys())
        all_categories = sorted(list(all_categories))
        
        predictions = {}
        
        # Predict for each category
        for category in all_categories:
            # Extract historical data for this category
            X = []
            y = []
            
            for i, month in enumerate(sorted_months):
                amount = monthly_breakdown[month].get(category, 0)
                X.append([i])
                y.append(amount)
            
            # Only predict if we have data for this category
            if any(y):  # If any non-zero values
                try:
                    # Use linear regression for simple trend
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    # Predict next month
                    next_month_index = len(sorted_months)
                    predicted = max(0, model.predict([[next_month_index]])[0])  # Prevent negative
                    
                    # Calculate R-squared as confidence
                    confidence = max(0, min(1, model.score(X, y)))
                    
                    predictions[category] = {
                        'predicted_amount': round(predicted, 2),
                        'trend': 'up' if model.coef_[0] > 0 else 'down',
                        'confidence': round(confidence, 2),
                        'historical_avg': round(sum(y) / len(y), 2)
                    }
                except:
                    predictions[category] = {
                        'predicted_amount': round(sum(y) / len(y), 2),
                        'trend': 'stable',
                        'confidence': 0.5,
                        'historical_avg': round(sum(y) / len(y), 2)
                    }
        
        # Calculate total prediction
        total_prediction = sum(p['predicted_amount'] for p in predictions.values())
        
        # Calculate overall confidence (average)
        if predictions:
            overall_confidence = round(
                sum(p['confidence'] for p in predictions.values()) / len(predictions), 
                2
            )
        else:
            overall_confidence = 0
        
        # Get current month for reference
        current_month = datetime.now()
        next_month = current_month.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
        
        return {
            'success': True,
            'current_month': current_month.strftime('%B %Y'),
            'predicted_month': next_month.strftime('%B %Y'),
            'total_prediction': round(total_prediction, 2),
            'by_category': predictions,
            'confidence': overall_confidence,
            'data_points': len(sorted_months)
        }
    
    def get_expense_trends(self):
        """Get expense trends for the last 6 months"""
        monthly_breakdown = self.get_monthly_breakdown()
        sorted_months = sorted(monthly_breakdown.keys())[-6:]  # Last 6 months
        
        trends = []
        for month in sorted_months:
            total = sum(monthly_breakdown[month].values())
            trends.append({
                'month': month,
                'total': round(total, 2),
                'breakdown': {k: round(v, 2) for k, v in monthly_breakdown[month].items()}
            })
        
        return trends

# Initialize predictor
predictor = MonthlyExpensePredictor()
