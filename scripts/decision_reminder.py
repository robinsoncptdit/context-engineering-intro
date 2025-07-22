#!/usr/bin/env python3
"""
Decision reminder - Can be called by Claude or manually
"""
import os
import sys
from datetime import datetime

def show_decision_reminder(context, change, original=None):
    """Display a decision reminder"""
    print("\n" + "="*60)
    print("📝 DECISION POINT DETECTED")
    print("="*60)
    print(f"\n🎯 Context: {context}")
    print(f"✨ Change: {change}")
    if original:
        print(f"📋 Original Plan: {original}")
    
    print("\n" + "-"*60)
    print("This seems like an important architectural decision!")
    print("\nYou have several options:")
    print("1. Quick decision:  python scripts/quick_decision.py")
    print("2. Full decision:   python scripts/add_decision.py")
    print("3. Skip for now:    Continue coding")
    print("\n💡 Tip: Document the 'why' - future you will thank you!")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Can be called with arguments or interactively
    if len(sys.argv) > 1:
        context = sys.argv[1]
        change = sys.argv[2] if len(sys.argv) > 2 else "Significant change"
        original = sys.argv[3] if len(sys.argv) > 3 else None
        show_decision_reminder(context, change, original)
    else:
        # Interactive mode
        show_decision_reminder(
            "Interactive Decision",
            "You and Claude agreed on a significant change",
            None
        )