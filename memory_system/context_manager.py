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
    
    def _get_current_milestone(self):
        """Get the current milestone from summaries"""
        summaries_dir = os.path.join(self.memory_dir, "summaries")
        if not os.path.exists(summaries_dir):
            return None
            
        # Find most recent milestone file
        milestone_files = [f for f in os.listdir(summaries_dir) 
                          if f.startswith("milestone-") and f.endswith(".md")]
        
        if not milestone_files:
            return None
            
        # Sort by modification time and get most recent
        latest = max(milestone_files, 
                    key=lambda f: os.path.getmtime(os.path.join(summaries_dir, f)))
        
        with open(os.path.join(summaries_dir, latest), 'r') as f:
            return f.read()
    
    def _get_recent_summaries(self, count=5):
        """Get recent session summaries"""
        summaries_dir = os.path.join(self.memory_dir, "summaries")
        if not os.path.exists(summaries_dir):
            return []
            
        # Find session summary files
        session_files = [f for f in os.listdir(summaries_dir) 
                        if f.startswith("session-") and f.endswith(".yaml")]
        
        if not session_files:
            return []
            
        # Sort by modification time and get most recent
        session_files.sort(key=lambda f: os.path.getmtime(
            os.path.join(summaries_dir, f)), reverse=True)
        
        summaries = []
        for file in session_files[:count]:
            with open(os.path.join(summaries_dir, file), 'r') as f:
                summaries.append(yaml.safe_load(f))
                
        return summaries
    
    def _analyze_prp_status(self, project_root):
        """Analyze project status against PRP requirements"""
        prp_path = os.path.join(project_root, "prp.md")
        status = {
            'has_prp': os.path.exists(prp_path),
            'last_modified': None,
            'drift_warnings': []
        }
        
        if status['has_prp']:
            status['last_modified'] = datetime.fromtimestamp(
                os.path.getmtime(prp_path)).isoformat()
            
            # Check for drift in recent decisions
            recent_decisions = self._get_recent_decisions(days=30)
            for decision in recent_decisions:
                if decision.get('drift_type') == 'major':
                    status['drift_warnings'].append({
                        'timestamp': decision['timestamp'],
                        'context': decision.get('context', 'Unknown'),
                        'impact': decision.get('impact', [])
                    })
        
        return status
    
    def _format_context_prompt(self, context):
        """Format context into a prompt for Claude Code"""
        prompt_parts = []
        
        # Header
        prompt_parts.append("## Current Context Summary")
        prompt_parts.append(f"Retrieved at: {datetime.now().isoformat()}\n")
        
        # Current milestone
        if context['current_milestone']:
            prompt_parts.append("## Current Milestone")
            prompt_parts.append(context['current_milestone'])
            prompt_parts.append("")
        
        # Recent decisions
        if context['recent_decisions']:
            prompt_parts.append("## Recent Decisions")
            for decision in context['recent_decisions']:
                prompt_parts.append(f"- **{decision.get('timestamp', 'Unknown')}**: {decision.get('context', 'No context')}")
                if decision.get('rationale'):
                    prompt_parts.append(f"  - Rationale: {decision['rationale']}")
                if decision.get('drift_type'):
                    prompt_parts.append(f"  - Drift Type: {decision['drift_type']}")
            prompt_parts.append("")
        
        # Recent work summaries
        if context['recent_summaries']:
            prompt_parts.append("## Recent Session Summaries")
            for summary in context['recent_summaries']:
                prompt_parts.append(f"\n### Session {summary.get('session_id', 'Unknown')}")
                prompt_parts.append(f"- Time: {summary.get('timestamp', 'Unknown')}")
                prompt_parts.append(f"- Files Modified: {', '.join(summary.get('files_modified', []))}")
                if summary.get('decisions'):
                    prompt_parts.append(f"- Decisions Made: {len(summary['decisions'])}")
            prompt_parts.append("")
        
        # PRP Status
        if context['prp_status']:
            prompt_parts.append("## PRP Status")
            status = context['prp_status']
            if status['has_prp']:
                prompt_parts.append(f"- PRP Document: Found (last modified: {status['last_modified']})")
                if status['drift_warnings']:
                    prompt_parts.append("- ⚠️ Drift Warnings:")
                    for warning in status['drift_warnings']:
                        prompt_parts.append(f"  - {warning['timestamp']}: {warning['context']}")
            else:
                prompt_parts.append("- PRP Document: Not found")
            prompt_parts.append("")
        
        # Active tasks reminder
        prompt_parts.append("## Next Steps")
        prompt_parts.append("Based on the context above, consider:")
        prompt_parts.append("1. Reviewing recent decisions for consistency")
        prompt_parts.append("2. Checking if current work aligns with PRP goals")
        prompt_parts.append("3. Identifying any incomplete tasks from recent sessions")
        
        return "\n".join(prompt_parts)
