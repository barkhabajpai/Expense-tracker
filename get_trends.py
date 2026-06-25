import json
import sys
sys.path.insert(0, '.')

from monthly_predictor import predictor

result = predictor.get_expense_trends()
print(json.dumps(result))
