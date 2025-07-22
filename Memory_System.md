# Memory System

## Step 1: First, Let's Get the Code

**Fork the Repository** (not clone) - This creates your own copy on GitHub:

1. Go to https://github.com/coleam00/context-engineering-intro
2. Click the "Fork" button in the top-right corner
3. Select your GitHub account as the destination
4. Wait for GitHub to create your fork

⠀
**Now Clone YOUR Fork** to your computer:

1. On your forked repo page, click the green "Code" button
2. Copy the URL shown
3. Open your terminal/command prompt
4. Navigate to where you want the project:

```
cd ~/Documents/Projects  # or wherever you keep code
```

5. Clone it:

```
git clone https://github.com/YOUR-USERNAME/context-engineering-intro.gitcd context-engineering-intro
```

⠀
## Step 2: Set Up Your Development Environment

1. **Install Required Tools** (if you don't have them):

```
# Check if you have Node.js
node --version

# If not, download from https://nodejs.org/

# Check if you have Python
python --version

# If not, download from https://python.org/
```

2. **Install Project Dependencies**:

```
# If the project has a package.json
npm install

# If it has requirements.txt
pip install -r requirements.txt
```

⠀
## Step 3: Create the Memory Architecture Structure

Create a new branch for your changes:

```
git checkout -b add-memory-architecture
```

Now let's build the memory system:

1. **Create the Memory Directory Structure**:

```
# From the project root
mkdir -p .claude-memory/summaries
mkdir -p .claude-memory/context-maps
mkdir -p .claude-memory/checkpoints
mkdir -p memory-system/src
```

2. **Create the Core Memory Files**:

3. Create `.claude-memory/decisions.yaml`:

```
# Decision and Drift Tracking Log
decisions: []
```

2. Create `memory-system/requirements.txt`:

```
neo4j==5.14.0
sentence-transformers==2.2.2
pyyaml==6.0.1
numpy==1.24.3
```

⠀
## Step 4: Build the Memory System Components

1. **Create the Semantic Code Graph** (`memory-system/src/semantic_graph.py`):

```
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import ast
import os

class SemanticCodeGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
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
```

2. **Create the Summary Generator** (`memory-system/src/summarizer.py`):

```
import os
import datetime
import yaml

class ProgressiveSummarizer:
    def __init__(self, memory_dir=".claude-memory"):
        self.memory_dir = memory_dir
        self.summaries_dir = os.path.join(memory_dir, "summaries")
        
    def create_session_summary(self, session_id, changes, decisions):
        """Create a summary of a coding session"""
        summary = {
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'changes': changes,
            'decisions': decisions,
            'files_modified': list(set([c['file'] for c in changes]))
        }
        
        filename = f"session-{session_id}.yaml"
        filepath = os.path.join(self.summaries_dir, filename)
        
        with open(filepath, 'w') as f:
            yaml.dump(summary, f)
        
        return summary
```

3. **Create the Context Reconstructor** (`memory-system/src/context_manager.py`):

```
import os
import yaml
from datetime import datetime, timedelta

class ContextManager:
    def __init__(self, memory_dir=".claude-memory"):
        self.memory_dir = memory_dir
        
    def reconstruct_context(self, project_root):
        """Reconstruct context for Claude Code"""
        context = {
            'current_milestone': self._get_current_milestone(),
            'recent_decisions': self._get_recent_decisions(days=7),
            'recent_summaries': self._get_recent_summaries(count=5),
            'prp_status': self._analyze_prp_status(project_root)
        }
        
        return self._format_context_prompt(context)
    
    def _get_recent_decisions(self, days):
        decisions_path = os.path.join(self.memory_dir, "decisions.yaml")
        if not os.path.exists(decisions_path):
            return []
            
        with open(decisions_path, 'r') as f:
            data = yaml.safe_load(f)
            
        cutoff = datetime.now() - timedelta(days=days)
        recent = [d for d in data.get('decisions', []) 
                 if datetime.fromisoformat(d['timestamp']) > cutoff]
        
        return recent
```

⠀
## Step 5: Create Integration Scripts

1. **Create the Main Integration Script** (`memory-system/integrate.py`):

```
#!/usr/bin/env python3
"""
Integration script to add memory capabilities to Claude Code sessions
"""
import sys
import os
from src.semantic_graph import SemanticCodeGraph
from src.summarizer import ProgressiveSummarizer
from src.context_manager import ContextManager

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
```

2. **Create a Claude Code Helper** (`memory-system/claude_helper.py`):

```
"""
Helper script to generate context for Claude Code
"""
from src.context_manager import ContextManager

def get_claude_context():
    cm = ContextManager()
    return cm.reconstruct_context(".")

if __name__ == "__main__":
    print(get_claude_context())
```

⠀
## Step 6: Create Documentation

Create `memory-system/README.md`:

```
# Claude Code Memory System

This system helps Claude Code maintain context across sessions and compaction events.

## Setup

1. Install Neo4j (for semantic code graph):
   - Download from https://neo4j.com/download/
   - Start with default settings

2. Install Python dependencies:
   ```bash
   cd memory-system
   pip install -r requirements.txt
```

1. Initialize memory for your project:

```
python memory-system/integrate.py /path/to/your/project
```

⠀
## Usage

### Before starting a Claude Code session:

```
python memory-system/claude_helper.py > context.md
```

Then include context.md in your Claude Code conversation.

### After each session:

Record important decisions and changes in `.claude-memory/decisions.yaml`.

## Components

* **Semantic Graph**: Stores code relationships
* **Summarizer**: Creates session summaries
* **Context Manager**: Reconstructs context for new sessions

```
## Step 7: Test Your System

1. **Test the setup**:
   ```bash
   cd memory-system
   python integrate.py ..
```

1. **Create a test script** (`memory-system/test_system.py`):

```
from src.summarizer import ProgressiveSummarizer# Test creating a summarysummarizer = ProgressiveSummarizer("../.claude-memory")summary = summarizer.create_session_summary(    "test-001",    [{"file": "test.py", "change": "Added function"}],    ["Decided to use PostgreSQL instead of SQLite"])print("Summary created:", summary)
```

⠀
## Step 8: Commit and Push Your Changes

1. **Add all new files**:

```
git add .
git status  # Check what's being added
```

2. **Commit your changes**:

```
git commit -m "Add Claude Code memory architecture system"
```

3. **Push to your fork**:

```
git push origin add-memory-architecture
```

⠀
## Step 9: Create a Pull Request (Optional)

If you want to share this with Cole:

1. Go to your fork on GitHub
2. Click "Pull requests" → "New pull request"
3. Make sure it's comparing your `add-memory-architecture` branch to Cole's `main`
4. Add a description explaining the memory system
5. Submit the PR

⠀
## Next Steps

To actually use this system:

1. **Before each Claude Code session**, run:

```
python memory-system/claude_helper.py > current_context.md
```

2. **Start your Claude Code session** with: "Here's my current project context: [paste current_context.md]"

3. **After each session**, update the decisions log and run the summarizer

⠀
This system will grow more powerful as you use it, building a rich semantic understanding of your codebase that persists across Claude Code sessions!