from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_model import categorizer
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/predict-category', methods=['POST'])
def predict_category():
    """
    Predict expense category based on description
    Expected JSON: {"description": "pizza for lunch"}
    """
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'Missing description field'}), 400
        
        description = data['description'].strip()
        
        if not description:
            return jsonify({'error': 'Description cannot be empty'}), 400
        
        result = categorizer.predict(description)
        
        if result is None:
            return jsonify({'error': 'Failed to predict category'}), 500
        
        # Return the prediction with all confidence scores
        response = {
            'category': result['category'],
            'confidence': result['confidence']
        }
        
        if 'all_predictions' in result:
            response['all_predictions'] = result['all_predictions']
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available expense categories"""
    try:
        categories = categorizer.get_categories()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ml-health', methods=['GET'])
def ml_health():
    """Health check for ML server"""
    return jsonify({'status': 'ML server is running'}), 200

if __name__ == '__main__':
    port = os.getenv('ML_PORT', 5001)
    print("\n" + "=" * 60)
    print("🚀 ML Server Starting")
    print("=" * 60)
    print(f"✅ Available Categories: {categorizer.get_categories()}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"📚 Training Samples: {len(categorizer.load_training_data()[0])}")
    print("=" * 60 + "\n")
    app.run(debug=False, port=int(port))
