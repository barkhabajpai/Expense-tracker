import json
import os
import joblib
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import warnings

warnings.filterwarnings('ignore')

class ExpenseCategorizer:
    def __init__(self, model_path='expense_model.pkl', vectorizer_path='vectorizer.pkl'):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.pipeline = None
        self.categories = []
        # Get the directory where this script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.expenses_file = os.path.join(self.script_dir, 'expenses.json')
        
    def load_training_data(self):
        """Load expenses from JSON file for training"""
        try:
            if os.path.exists(self.expenses_file):
                with open(self.expenses_file, 'r') as f:
                    expenses = json.load(f)
                    
                descriptions = [exp.get('description', '').lower() for exp in expenses]
                categories = [exp.get('category', 'Other') for exp in expenses]
                
                return descriptions, categories
        except Exception as e:
            print(f"Error loading training data: {e}")
        return [], []
    
    def train(self):
        """Train the logistic regression model"""
        descriptions, categories = self.load_training_data()
        
        if len(descriptions) < 2:
            print("Insufficient training data. Model requires at least 2 samples.")
            return False
        
        self.categories = list(set(categories))
        
        try:
            # Create a pipeline with TF-IDF vectorizer and Logistic Regression
            self.pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=100, 
                    lowercase=True, 
                    stop_words='english',
                    min_df=1,
                    max_df=0.95,
                    ngram_range=(1, 2)  # Use unigrams and bigrams
                )),
                ('clf', LogisticRegression(max_iter=200, random_state=42, C=1.0))
            ])
            
            # Train the model
            self.pipeline.fit(descriptions, categories)
            
            # Save the model
            joblib.dump(self.pipeline, self.model_path)
            
            # Print training statistics
            print(f"✅ Model trained successfully!")
            print(f"📊 Categories found: {self.categories}")
            print(f"📈 Training samples: {len(descriptions)}")
            print(f"🎯 Model saved to: {self.model_path}")
            
            return True
        except Exception as e:
            print(f"❌ Error training model: {e}")
            return False
    
    def predict(self, description):
        """Predict category for a given expense description"""
        # Load model if not already loaded
        if self.pipeline is None:
            if os.path.exists(self.model_path):
                try:
                    self.pipeline = joblib.load(self.model_path)
                except Exception as e:
                    print(f"Error loading model: {e}")
                    return None
            else:
                # If model doesn't exist, train it
                if not self.train():
                    return None
        
        try:
            description = description.lower().strip()
            if not description:
                return None
            
            # Get prediction and probabilities
            prediction = self.pipeline.predict([description])[0]
            probabilities = self.pipeline.predict_proba([description])[0]
            confidence = float(max(probabilities))
            
            # Get all class labels and their probabilities
            classes = self.pipeline.classes_
            
            result = {
                'category': prediction,
                'confidence': round(confidence, 2),
                'all_predictions': {}
            }
            
            # Add all category predictions sorted by confidence
            for i, class_label in enumerate(classes):
                result['all_predictions'][class_label] = round(float(probabilities[i]), 2)
            
            # Sort predictions by confidence
            result['all_predictions'] = dict(sorted(
                result['all_predictions'].items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
            
            return result
        except Exception as e:
            print(f"Error predicting category: {e}")
            return None
    
    def get_categories(self):
        """Get all available categories"""
        if not self.categories:
            descriptions, categories = self.load_training_data()
            self.categories = list(set(categories))
        return self.categories

# Initialize the categorizer
categorizer = ExpenseCategorizer()

# Train on startup
print("=" * 60)
print("🤖 Initializing ML Model for Expense Categorization")
print("=" * 60)
categorizer.train()
print("=" * 60)
