
import json
from datetime import datetime

def assess_risk(processed_data):
    risk_levels = {
        'Low': 0.3,
        'Medium': 0.6,
        'High': 0.9
    }
    
    risk_assessment = {
        'timestamp': datetime.now().isoformat(),
        'assessments': [],
        'metadata': {
            'model': 'ThreatLevelAI',
            'version': '1.0'
        }
    }
    
    for category, objects in processed_data['objects'].items():
        for obj in objects:
            risk_level = calculate_risk_level(category, obj)
            risk_assessment['assessments'].append({
                'object_id': obj['id'],
                'category': category,
                'risk_level': risk_level,
                'confidence': obj['confidence'],
                'threat_score': risk_levels[risk_level]
            })
    
    return risk_assessment

def calculate_risk_level(category, obj):
    if category in ['uaps', 'usos'] and obj['confidence'] > 0.7:
        return 'High'
    elif category == 'aircraft' and obj['type'] == 'commercial_aircraft':
        return 'Low'
    elif category == 'space_debris' and obj['confidence'] > 0.8:
        return 'Medium'
    else:
        return 'Low'

def main():
    try:
        with open('processed_tracking_data.json', 'r') as f:
            processed_data = json.load(f)
        
        risk_evaluation = assess_risk(processed_data)
        
        with open('risk_evaluation.json', 'w') as f:
            json.dump(risk_evaluation, f, indent=2)
            
    except Exception as e:
        print(f"Error in risk assessment: {e}")

if __name__ == "__main__":
    main()
