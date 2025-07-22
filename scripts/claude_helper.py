"""
Helper script to generate context for Claude Code
"""
import os
import sys

# Add parent directory to path to find memory_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_system.context_manager import ContextManager

def get_claude_context():
    cm = ContextManager()
    return cm.reconstruct_context(".")

if __name__ == "__main__":
    print(get_claude_context())
