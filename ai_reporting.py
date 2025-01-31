
import json
from datetime import datetime
import time

def generate_reports(recommendations_data):
    reports = {
        'timestamp': datetime.now().isoformat(),
        'reports': {
            'policy': generate_policy_report(recommendations_data),
            'scientific': generate_scientific_report(recommendations_data),
            'public': generate_public_report(recommendations_data),
            'military': generate_military_report(recommendations_data)
        },
        'metadata': {
            'generator': 'AI_ReportingSystem',
            'version': '1.0'
        }
    }
    return reports

def generate_policy_report(data):
    return {
        'type': 'policy',
        'summary': 'Policy implications of detected anomalies',
        'recommendations': data.get('policy_recommendations', []),
        'priority_level': calculate_priority(data)
    }

def generate_scientific_report(data):
    return {
        'type': 'scientific',
        'analysis': 'Scientific analysis of detected phenomena',
        'data_points': len(data.get('policy_recommendations', [])),
        'confidence_levels': extract_confidence_levels(data)
    }

def generate_public_report(data):
    return {
        'type': 'public',
        'summary': 'Public information release',
        'safety_status': get_safety_status(data),
        'last_updated': datetime.now().isoformat()
    }

def generate_military_report(data):
    return {
        'type': 'military',
        'threat_assessment': 'Classified threat assessment',
        'response_protocols': get_response_protocols(data),
        'classified_level': 'TOP_SECRET'
    }

def calculate_priority(data):
    high_risk_count = sum(1 for rec in data.get('policy_recommendations', [])
                         if rec.get('threat_score', 0) > 0.7)
    return 'HIGH' if high_risk_count > 0 else 'MEDIUM'

def extract_confidence_levels(data):
    return [rec.get('threat_score', 0) 
            for rec in data.get('policy_recommendations', [])]

def get_safety_status(data):
    threat_scores = [rec.get('threat_score', 0) 
                    for rec in data.get('policy_recommendations', [])]
    avg_threat = sum(threat_scores) / len(threat_scores) if threat_scores else 0
    return 'NORMAL' if avg_threat < 0.5 else 'ELEVATED'

def get_response_protocols(data):
    protocols = []
    for rec in data.get('policy_recommendations', []):
        protocols.extend(rec.get('actions', []))
    return list(set(protocols))

def main():
    while True:
        try:
            with open('governance_recommendations.json', 'r') as f:
                recommendations = json.load(f)
            
            reports = generate_reports(recommendations)
            
            with open('real_time_reports.json', 'w') as f:
                json.dump(reports, f, indent=2)
                
        except Exception as e:
            print(f"Error in report generation: {e}")
            
        time.sleep(3600)  # Run every hour as per tasks.json

if __name__ == "__main__":
    main()
