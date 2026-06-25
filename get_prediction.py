import json
import sys
sys.path.insert(0, '.')

from monthly_predictor import predictor

result = predictor.predict_next_month()
print(json.dumps(result))
