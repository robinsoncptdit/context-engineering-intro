# Instructions for Claude Code

## Memory System Integration

You are working on a project with a memory system. Please follow these practices:

### 1. Decision Detection

When you and the user agree on any of these changes, **remind them to document it**:

- Switching technologies/frameworks
- Adding major dependencies  
- Changing architecture patterns
- Deviating from original plans
- Adding unplanned features
- Making performance trade-offs

### 2. Reminder Format

When detecting a decision point, say:

```
📝 DECISION POINT: [What we're changing]

We just agreed to: [specific change]
This impacts: [what parts of the code]

Would you like to document this decision?
→ Quick: python scripts/quick_decision.py
→ Full: python scripts/add_decision.py
```

### 3. Context Awareness

At the start of each session, if you receive a context file, acknowledge:
- Recent decisions made
- Any drift warnings
- Current milestone status

### 4. End of Session

Before the user leaves, remind them:
- Any undocumented decisions from this session
- To run: `python scripts/claude_helper.py > context.md`
- To commit their changes with meaningful messages

### 5. Keywords to Watch For

These phrases often indicate decision points:
- "Let's use X instead of Y"
- "Actually, a better approach would be..."
- "Let's also add..."
- "We should change..."
- "On second thought..."
- "Let's switch to..."

## Example Interaction

User: "Let's use PostgreSQL instead of SQLite for better performance"

Claude: "I'll help you set up PostgreSQL. 

📝 DECISION POINT: Database Technology Change

We just agreed to: Switch from SQLite to PostgreSQL
This impacts: Models, database configuration, deployment

Would you like to document this decision?
→ Quick: python scripts/quick_decision.py

[Then continue with implementation...]"