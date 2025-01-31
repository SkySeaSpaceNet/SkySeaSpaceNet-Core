
import subprocess
import sys

def start_components():
    components = [
        'ai_data_processing.py',
        'ai_risk_assessment.py',
        'ai_governance.py',
        'ai_governance_decision.py',
        'ai_reporting.py',
        'ai_storage.py'
    ]
    
    processes = []
    for component in components:
        try:
            process = subprocess.Popen([sys.executable, component])
            processes.append(process)
            print(f"Started {component}")
        except Exception as e:
            print(f"Error starting {component}: {e}")
    
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    start_components()
