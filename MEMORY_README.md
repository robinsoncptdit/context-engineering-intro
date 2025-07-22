# Claude Code Memory System

A persistent context management system for maintaining continuity across Claude Code sessions.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize memory system**:
   ```bash
   python scripts/integrate.py
   ```

3. **Before starting Claude Code**:
   ```bash
   python scripts/claude_helper.py > context.md
   ```
   Then include context.md in your conversation.

## Project Structure

```
context-engineering-intro/
├── .claude-memory/          # Memory storage (auto-created)
│   ├── decisions.yaml       # Architectural decisions & drift log
│   └── summaries/          # Session summaries
├── memory_system/          # Core Python package
│   ├── __init__.py
│   ├── context_manager.py  # Context reconstruction
│   ├── semantic_graph.py   # Neo4j code graph (optional)
│   └── summarizer.py       # Session summarization
├── scripts/                # Utility scripts
│   ├── integrate.py        # Setup script
│   ├── claude_helper.py    # Context generator
│   └── test_system.py      # Test suite
└── requirements.txt        # Python dependencies
```

## How It Works

1. **Context Manager**: Reconstructs relevant context from past sessions
2. **Summarizer**: Creates hierarchical summaries of coding sessions
3. **Decision Tracking**: Logs architectural decisions and drift from plans
4. **Semantic Graph** (optional): Neo4j-based code relationship tracking

## Usage Examples

### Track a Decision
Add to `.claude-memory/decisions.yaml`:
```yaml
decisions:
  - timestamp: 2024-11-20T10:30:00
    context: "Authentication implementation"
    prp_requirement: "Basic auth"
    actual_implementation: "OAuth2"
    drift_type: "enhancement"
    rationale: "Better security"
```

### Create Session Summary
```python
from memory_system import ProgressiveSummarizer

summarizer = ProgressiveSummarizer()
summarizer.create_session_summary(
    session_id="auth-work",
    changes=[{"file": "auth.py", "change": "Added OAuth"}],
    decisions=["Switched to OAuth2"]
)
```

## Testing

```bash
python scripts/test_system.py
```

## Requirements

- Python 3.8+
- Neo4j (optional, for semantic graph)
- See requirements.txt for packages