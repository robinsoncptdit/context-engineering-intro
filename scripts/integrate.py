#!/usr/bin/env python3
"""
Integration script to add memory capabilities to Claude Code sessions
"""
import sys
import os

# Add parent directory to path to find memory_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_system.semantic_graph import SemanticCodeGraph
from memory_system.summarizer import ProgressiveSummarizer
from memory_system.context_manager import ContextManager

def setup_memory_system(project_root):
    """Initialize the memory system for a project"""
    memory_dir = os.path.join(project_root, ".claude-memory")
    
    # Create directories
    os.makedirs(memory_dir, exist_ok=True)
    os.makedirs(os.path.join(memory_dir, "summaries"), exist_ok=True)
    
    # Initialize components
    print("✓ Memory directories created")
    
    # Create initial decisions file
    decisions_file = os.path.join(memory_dir, "decisions.yaml")
    if not os.path.exists(decisions_file):
        with open(decisions_file, 'w') as f:
            f.write("decisions: []\n")
    
    print("✓ Memory system initialized")
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        setup_memory_system(sys.argv[1])
    else:
        setup_memory_system(os.getcwd())
