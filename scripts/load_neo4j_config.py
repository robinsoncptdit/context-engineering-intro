#!/usr/bin/env python3
"""
Load Neo4j configuration from .neo4j_config file
"""
import os

def load_neo4j_config():
    """Load Neo4j configuration from .neo4j_config file"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.neo4j_config')
    
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    # Set environment variables
    for key, value in config.items():
        os.environ[key] = value
    
    return config

if __name__ == "__main__":
    config = load_neo4j_config()
    print("Loaded Neo4j config:")
    for key, value in config.items():
        if 'PASSWORD' in key:
            print(f"  {key}: ***hidden***")
        else:
            print(f"  {key}: {value}")