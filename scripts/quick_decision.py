#!/usr/bin/env python3
"""
Quick decision entry - minimal prompts for fast documentation
"""
import os
import sys
import yaml
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def quick_decision():
    """Quick decision entry with minimal prompts"""
    decisions_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.claude-memory', 'decisions.yaml')
    
    # Load existing
    if os.path.exists(decisions_file):
        with open(decisions_file, 'r') as f:
            data = yaml.safe_load(f) or {'decisions': []}
    else:
        data = {'decisions': []}
    
    print("\n⚡ Quick Decision Entry")
    print("=" * 30)
    
    # Minimal inputs
    context = input("What area? (e.g., auth, database): ").strip()
    if not context:
        print("Cancelled.")
        return
        
    change = input("What changed?: ").strip()
    if not change:
        print("Cancelled.")
        return
        
    why = input("Why?: ").strip()
    if not why:
        why = "Performance/UX improvement"
    
    # Quick decision
    decision = {
        'timestamp': datetime.now().isoformat(),
        'context': context,
        'actual_implementation': change,
        'rationale': why,
        'drift_type': 'enhancement',
        'approved': True
    }
    
    # Add and save
    data['decisions'].insert(0, decision)
    
    with open(decisions_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    print(f"\n✅ Saved: {context} - {change}")

if __name__ == "__main__":
    try:
        quick_decision()
    except KeyboardInterrupt:
        print("\nCancelled.")