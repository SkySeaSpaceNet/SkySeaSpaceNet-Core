import json
import time
from datetime import datetime

def process_governance_decisions(recommendations):
    decisions = {
        'timestamp': datetime.now().isoformat(),
        'decisions': [],
        'metadata': {
            'framework': 'autonomous_governance',
            'version': '2.0'
        }
    }

    for rec in recommendations.get('policy_recommendations', []):
        if validate_autonomous_decision(rec):
            decision = {
                'object_id': rec['object_id'],
                'category': rec['category'],
                'threat_score': rec['threat_score'],
                'approved_actions': evaluate_and_approve_actions(rec),
                'status': 'autonomous_execution',
                'decision_rationale': generate_decision_rationale(rec),
                'safety_checks_passed': True
            }
            execute_approved_actions(decision)
        else:
            decision = {
                'object_id': rec['object_id'],
                'category': rec['category'],
                'threat_score': rec['threat_score'],
                'status': 'requires_human_review',
                'decision_rationale': 'Autonomous decision validation failed'
            }
        decisions['decisions'].append(decision)

    return decisions

def evaluate_and_approve_actions(recommendation):
    approved_actions = []
    risk_weights = {
        'uaps': 0.9,
        'usos': 0.85,
        'aircraft': 0.6,
        'satellites': 0.7,
        'space_debris': 0.5
    }

    for action in recommendation.get('actions', []):
        weighted_risk = recommendation['threat_score'] * risk_weights.get(recommendation['category'], 0.5)
        if validate_action_safety(action) and weighted_risk < 0.8:
            approved_actions.append({
                'action': action,
                'approval_status': 'approved',
                'risk_score': weighted_risk,
                'timestamp': datetime.now().isoformat()
            })
        else:
            approved_actions.append({
                'action': action,
                'approval_status': 'requires_human_review',
                'risk_score': weighted_risk,
                'timestamp': datetime.now().isoformat()
            })
    return approved_actions

def validate_action_safety(action):
    unsafe_keywords = ['override', 'disable', 'shutdown', 'weapon']
    return not any(keyword in action.lower() for keyword in unsafe_keywords)

def generate_decision_rationale(recommendation):
    category_rationales = {
        'uaps': 'Potential aerospace safety risk requiring immediate attention',
        'usos': 'Underwater anomaly requiring naval coordination',
        'aircraft': 'Aviation safety protocol activation',
        'satellites': 'Space traffic management response',
        'space_debris': 'Orbital debris mitigation protocol'
    }
    return category_rationales.get(recommendation['category'], 'Standard protocol implementation')

def validate_autonomous_decision(recommendation):
    safety_conditions = [
        recommendation['threat_score'] < 0.6,
        recommendation['category'] not in ['uaps', 'usos'],
        not any(keyword in str(recommendation).lower() for keyword in ['weapon', 'military', 'override', 'emergency'])
    ]
    return all(safety_conditions)

def execute_approved_actions(decision):
    try:
        with open('autonomous_actions_log.json', 'a') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'action': decision,
                'execution_status': 'completed'
            }, f)
            f.write('\n')
    except Exception as e:
        print(f"Error executing autonomous action: {e}")

def main():
    while True:
        try:
            with open('governance_recommendations.json', 'r') as f:
                recommendations = json.load(f)

            decisions = process_governance_decisions(recommendations)

            with open('ai_decision_log.json', 'w') as f:
                json.dump(decisions, f, indent=2)

        except Exception as e:
            print(f"Error in decision processing: {e}")

        time.sleep(21600)  # Run every 6 hours as per tasks.json

if __name__ == "__main__":
    main()