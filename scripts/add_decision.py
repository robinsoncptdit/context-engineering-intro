#!/usr/bin/env python3
"""
Interactive script to add decisions to decisions.yaml
"""
import os
import sys
import yaml
from datetime import datetime

# Add parent directory to path to find memory_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("This field is required. Please enter a value.")

def get_multiline_input(prompt):
    """Get multiline input from user"""
    print(f"{prompt} (Enter 'done' on a new line when finished):")
    lines = []
    while True:
        line = input()
        if line.strip().lower() == 'done':
            break
        lines.append(line)
    return '\n'.join(lines) if lines else ''

def get_list_input(prompt):
    """Get list input from user"""
    print(f"{prompt} (Enter each item on a new line, 'done' when finished):")
    items = []
    while True:
        item = input("  - ").strip()
        if item.lower() == 'done':
            break
        if item:
            items.append(item)
    return items

def add_decision():
    """Interactive decision entry"""
    print("\n🧠 Claude Memory System - Add Decision")
    print("=" * 50)
    print("\nThis tool helps you document important architectural decisions,")
    print("technology changes, or significant deviations from your original plan.\n")
    
    # Load existing decisions
    decisions_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.claude-memory', 'decisions.yaml')
    
    if os.path.exists(decisions_file):
        with open(decisions_file, 'r') as f:
            data = yaml.safe_load(f) or {'decisions': []}
    else:
        data = {'decisions': []}
    
    # Check if user wants to proceed
    proceed = input("Do you want to add a new decision? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Cancelled.")
        return
    
    print("\n📝 Enter decision details:\n")
    
    # Gather decision information
    decision = {
        'timestamp': datetime.now().isoformat(),
        'context': get_input("Context (e.g., 'User authentication', 'Database design')"),
        'prp_requirement': get_input("Original requirement/plan", "Not specified"),
        'actual_implementation': get_input("What was actually implemented"),
        'drift_type': get_input("Drift type", "enhancement").lower(),
        'rationale': get_input("Why did you make this change?"),
        'impact': get_list_input("What other parts of the code were affected?"),
        'approved': get_input("Is this change approved? (y/n)", "y").lower() == 'y'
    }
    
    # Show preview
    print("\n📋 Decision Preview:")
    print("-" * 50)
    print(f"Timestamp: {decision['timestamp']}")
    print(f"Context: {decision['context']}")
    print(f"Original: {decision['prp_requirement']}")
    print(f"Actual: {decision['actual_implementation']}")
    print(f"Drift Type: {decision['drift_type']}")
    print(f"Rationale: {decision['rationale']}")
    print(f"Impact: {', '.join(decision['impact']) if decision['impact'] else 'None'}")
    print(f"Approved: {'Yes' if decision['approved'] else 'No'}")
    print("-" * 50)
    
    # Confirm
    confirm = input("\nSave this decision? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Add to decisions list (at the beginning)
    data['decisions'].insert(0, decision)
    
    # Save
    os.makedirs(os.path.dirname(decisions_file), exist_ok=True)
    with open(decisions_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    print("\n✅ Decision saved successfully!")
    print(f"📁 Location: {decisions_file}")
    
    # Offer to generate context
    gen_context = input("\nGenerate updated context for Claude? (y/n): ").strip().lower()
    if gen_context == 'y':
        os.system('python scripts/claude_helper.py > current_context.md')
        print("✅ Context updated in current_context.md")

if __name__ == "__main__":
    try:
        add_decision()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please make sure you're in the project directory.")