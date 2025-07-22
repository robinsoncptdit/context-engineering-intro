#!/usr/bin/env python3
"""
Test Neo4j connection
"""
import os
import sys

# Add parent directory to path to find memory_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_system.semantic_graph import SemanticCodeGraph

def test_neo4j_connection():
    """Test connection to Neo4j database"""
    
    # Get credentials
    password = input("Enter your Neo4j password (default was 'neo4j'): ")
    
    print("\nTesting connection to Neo4j...")
    
    try:
        # Try with bolt protocol (standard)
        graph = SemanticCodeGraph(
            uri="bolt://localhost:7687",
            user="neo4j",
            password=password
        )
        
        # Test by adding a sample entity
        graph.add_code_entity(
            file_path="test.py",
            entity_type="function",
            name="test_function",
            code="def test_function():\n    return 'Hello Neo4j!'",
            purpose="Test connection to Neo4j"
        )
        
        print("✅ Successfully connected to Neo4j!")
        print("   - Added test entity to graph")
        
        # Clean up
        with graph.driver.session() as session:
            session.run("MATCH (n:CodeEntity {name: 'test_function'}) DELETE n")
        
        graph.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Neo4j is running in Neo4j Desktop")
        print("2. Check that the database is started (green play button)")
        print("3. Verify your password is correct")
        print("4. Default connection is bolt://localhost:7687")

if __name__ == "__main__":
    test_neo4j_connection()