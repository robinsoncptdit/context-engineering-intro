#!/usr/bin/env python3
"""
Test script for Claude Code Memory System
"""
import os
import sys
import datetime

# Add parent directory to path to find memory_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Neo4j config if available
from load_neo4j_config import load_neo4j_config
load_neo4j_config()

from memory_system.summarizer import ProgressiveSummarizer
from memory_system.context_manager import ContextManager
from memory_system.semantic_graph import SemanticCodeGraph

def test_summarizer():
    """Test creating a summary"""
    print("Testing ProgressiveSummarizer...")
    
    # Create a test summary
    summarizer = ProgressiveSummarizer(".claude-memory")
    
    test_changes = [
        {"file": "test.py", "change": "Added authentication function"},
        {"file": "models.py", "change": "Created User model"},
        {"file": "routes.py", "change": "Added login endpoint"}
    ]
    
    test_decisions = [
        "Decided to use JWT tokens for authentication",
        "Chose PostgreSQL over SQLite for production readiness"
    ]
    
    summary = summarizer.create_session_summary(
        "test-001",
        test_changes,
        test_decisions
    )
    
    print(f"✓ Summary created: {summary['session_id']}")
    print(f"  - Timestamp: {summary['timestamp']}")
    print(f"  - Files modified: {', '.join(summary['files_modified'])}")
    print(f"  - Decisions: {len(summary['decisions'])}")
    
    return summary

def test_context_manager():
    """Test context reconstruction"""
    print("\nTesting ContextManager...")
    
    cm = ContextManager(".claude-memory")
    
    # First, create a test decision
    decisions_path = os.path.join(".claude-memory", "decisions.yaml")
    test_decision = {
        'timestamp': datetime.datetime.now().isoformat(),
        'context': 'Test decision for authentication system',
        'prp_requirement': 'Basic email/password auth',
        'actual_implementation': 'Added JWT-based auth with refresh tokens',
        'drift_type': 'enhancement',
        'rationale': 'Better security and user experience',
        'impact': ['Added pyjwt dependency', 'Modified auth flow'],
        'approved': True
    }
    
    # Load existing decisions or create new
    import yaml
    if os.path.exists(decisions_path):
        with open(decisions_path, 'r') as f:
            data = yaml.safe_load(f) or {'decisions': []}
    else:
        data = {'decisions': []}
    
    data['decisions'].append(test_decision)
    
    with open(decisions_path, 'w') as f:
        yaml.dump(data, f)
    
    print("✓ Added test decision to decisions.yaml")
    
    # Test context reconstruction
    context = cm.reconstruct_context(".")
    
    print("✓ Context reconstructed successfully")
    print("\nGenerated context prompt preview:")
    print("-" * 50)
    print(context[:500] + "..." if len(context) > 500 else context)
    print("-" * 50)
    
    return context

def test_semantic_graph():
    """Test semantic code graph (requires Neo4j)"""
    print("\nTesting SemanticCodeGraph...")
    
    try:
        # Try to connect to Neo4j
        graph = SemanticCodeGraph()
        
        # Add a test entity
        graph.add_code_entity(
            file_path="test_auth.py",
            entity_type="function",
            name="authenticate_user",
            code="""def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return generate_jwt_token(user)
    return None""",
            purpose="Authenticate user with email and password, return JWT token"
        )
        
        print("✓ Successfully added code entity to graph")
        graph.close()
        
    except Exception as e:
        print(f"⚠️  Neo4j connection failed: {str(e)}")
        print("   Make sure Neo4j is running on localhost:7687")
        print("   Continuing with other tests...")

def test_integration():
    """Test full integration"""
    print("\nTesting Full Integration...")
    
    # Simulate a complete workflow
    print("1. Creating session summary...")
    summary = test_summarizer()
    
    print("\n2. Testing context reconstruction...")
    context = test_context_manager()
    
    print("\n3. Testing semantic graph...")
    test_semantic_graph()
    
    print("\n✅ All tests completed!")
    print("\nTo use in production:")
    print("1. Run: python scripts/integrate.py /path/to/project")
    print("2. Before Claude session: python scripts/claude_helper.py > context.md")
    print("3. After session: Update decisions.yaml and create session summaries")

if __name__ == "__main__":
    # Ensure memory directories exist
    os.makedirs(".claude-memory/summaries", exist_ok=True)
    
    print("Claude Code Memory System Test Suite")
    print("=" * 50)
    
    test_integration()