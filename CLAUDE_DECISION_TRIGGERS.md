# Claude Decision Triggers

## When to Document a Decision

### 🚨 Automatic Triggers (Claude should remind you):

1. **Architecture Changes**
   - "Let's switch from X to Y" → DECISION
   - "We should use [new technology]" → DECISION
   - "Let's refactor the entire..." → DECISION

2. **Deviation from Plan**
   - "Instead of [original plan], let's..." → DECISION
   - "Actually, a better approach would be..." → DECISION
   - "The PRP says X but we'll do Y" → DECISION

3. **Major Dependencies**
   - "Let's add [new library/framework]" → DECISION
   - "We need to install..." → DECISION
   - "This requires [external service]" → DECISION

4. **Scope Changes**
   - "Let's also add [new feature]" → DECISION
   - "We should include..." → DECISION
   - "While we're at it..." → DECISION

## Claude Reminder Template

When Claude detects a decision point, it should say:

```
📝 DECISION POINT: [Brief description]

We just agreed to: [specific change]
This differs from: [original plan/approach]

Should I help you document this decision? 
Run: python scripts/add_decision.py
```

## Keywords That Trigger Reminders

### High Priority (Always remind):
- "let's switch to"
- "let's use ... instead"
- "better approach would be"
- "let's change the architecture"
- "we should refactor"
- "let's add [major feature]"

### Medium Priority (Remind if significant):
- "let's also add"
- "we could improve this by"
- "actually, let's"
- "on second thought"
- "let's go with"

### Context Clues:
- Multiple files being modified
- New dependencies being added
- Changing core functionality
- Deviating from documented plans