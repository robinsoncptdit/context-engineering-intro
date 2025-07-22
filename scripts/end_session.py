#!/usr/bin/env python3
"""
End a Claude Code session - create summary and prepare for next session
"""
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_system import ProgressiveSummarizer

def end_session():
    """Interactive session ending"""
    print("\n🏁 Ending Claude Code Session")
    print("=" * 50)
    
    # Get session info
    session_id = input("Session name (e.g., 'auth-work'): ").strip()
    if not session_id:
        session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M')}"
        print(f"Using default: {session_id}")
    
    # Get changes
    print("\nWhat files did you modify? (enter 'done' when finished)")
    changes = []
    while True:
        file = input("File: ").strip()
        if file.lower() == 'done' or not file:
            break
        change = input(f"What changed in {file}?: ").strip()
        if change:
            changes.append({"file": file, "change": change})
    
    # Get decisions made
    print("\nWhat decisions were made? (enter 'done' when finished)")
    decisions = []
    while True:
        decision = input("Decision: ").strip()
        if decision.lower() == 'done' or not decision:
            break
        decisions.append(decision)
    
    # Create summary
    if changes or decisions:
        summarizer = ProgressiveSummarizer()
        summary = summarizer.create_session_summary(session_id, changes, decisions)
        
        print("\n✅ Session summary created!")
        print(f"📁 Saved as: session-{session_id}.yaml")
        
        # Generate new context
        generate = input("\nGenerate context for next session? (y/n): ").strip().lower()
        if generate == 'y':
            os.system('python scripts/claude_helper.py > current_context.md')
            print("✅ Context ready in current_context.md")
            print("\n🚀 Ready for your next Claude Code session!")
    else:
        print("\nNo changes or decisions recorded. Session not saved.")

if __name__ == "__main__":
    try:
        end_session()
    except KeyboardInterrupt:
        print("\n\nSession ending cancelled.")