from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import ast
import os

class SemanticCodeGraph:
    def __init__(self, uri=None, user=None, password=None):
        # Try to load from environment or use defaults
        if not uri:
            uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        if not user:
            user = os.getenv('NEO4J_USER', 'neo4j')
        if not password:
            password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def add_code_entity(self, file_path, entity_type, name, code, purpose):
        """Add a code entity (function/class) to the graph"""
        embedding = self.encoder.encode(f"{purpose}\n{code}").tolist()
        
        with self.driver.session() as session:
            session.run("""
                CREATE (n:CodeEntity {
                    file: $file,
                    type: $type,
                    name: $name,
                    code: $code,
                    purpose: $purpose,
                    embedding: $embedding,
                    created: timestamp()
                })
            """, file=file_path, type=entity_type, name=name, 
                 code=code, purpose=purpose, embedding=embedding)
    
    def close(self):
        self.driver.close()
