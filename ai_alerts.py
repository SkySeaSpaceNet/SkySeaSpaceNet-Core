
import json
import time
from datetime import datetime

def generate_alert(risk_assessment):
    alert = {
        'timestamp': datetime.now().isoformat(),
        'alerts': [],
        'metadata': {
            'alert_system': 'matrix_p2p',
            'version': '1.0'
        }
    }
    
    for assessment in risk_assessment['assessments']:
        if assessment['risk_level'] == 'High':
            alert['alerts'].append({
                'object_id': assessment['object_id'],
                'category': assessment['category'],
                'threat_score': assessment['threat_score'],
                'message': generate_alert_message(assessment)
            })
    
    return alert

def generate_alert_message(assessment):
    category_messages = {
        'uaps': 'Unidentified Aerial Phenomenon detected',
        'usos': 'Unidentified Submerged Object detected',
        'aircraft': 'Unregistered aircraft detected',
        'satellites': 'Satellite anomaly detected'
    }
    
    base_message = category_messages.get(assessment['category'], 'Unknown anomaly detected')
    return f"{base_message} - Threat Score: {assessment['threat_score']}"

def main():
    while True:
        try:
            with open('risk_evaluation.json', 'r') as f:
                risk_data = json.load(f)
            
            alert = generate_alert(risk_data)
            
            with open('alert_status.json', 'w') as f:
                json.dump(alert, f, indent=2)
                
        except Exception as e:
            print(f"Error in alert generation: {e}")
            
        time.sleep(1)  # Check every second for high-risk events

if __name__ == "__main__":
    main()
